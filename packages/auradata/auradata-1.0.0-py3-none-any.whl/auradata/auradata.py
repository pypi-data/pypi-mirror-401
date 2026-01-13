import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
import json
from datetime import datetime
import warnings

# Optional imports for PDF generation
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import seaborn as sns
    from matplotlib.backends.backend_pdf import PdfPages
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

class Dataset:
    def __init__(self, X, y=None, feature_names=None):
        if not isinstance(X, pd.DataFrame):
            self.X = pd.DataFrame(X, columns=feature_names)
        else:
            self.X = X.copy()
            if feature_names:
                self.X.columns = feature_names
        
        self.y = pd.Series(y).reset_index(drop=True) if y is not None else None
        
        if self.y is not None and len(self.X) != len(self.y):
            raise ValueError(f"X and y length mismatch: {len(self.X)} vs {len(self.y)}")
        
        self.X_original = self.X.copy()
        self.y_original = self.y.copy() if y is not None else None
        
        self.issues = {}
        self.cleaned = False
        self.labels_fixed = False
        self._feature_subset = None

    def _find_duplicates(self):
        return self.X.duplicated(keep='first')

    def _find_noise(self, contamination=0.05):
        numeric_X = self.X.select_dtypes(include=[np.number])
        
        if numeric_X.shape[1] == 0:
            warnings.warn("No numeric columns found. Skipping noise detection.")
            return pd.Series(False, index=self.X.index)
        
        if len(numeric_X) < 10:
            warnings.warn("Dataset too small for reliable noise detection.")
            return pd.Series(False, index=self.X.index)

        try:
            iso = IsolationForest(contamination=contamination, random_state=0, n_jobs=-1)
            predictions = iso.fit_predict(numeric_X)
            return pd.Series(predictions == -1, index=self.X.index)
        except Exception as e:
            warnings.warn(f"Noise detection failed: {e}")
            return pd.Series(False, index=self.X.index)

    def _find_label_issues(self, model, threshold=0.6, feature_subset=None):
        if self.y is None:
            return pd.Series(False, index=self.X.index)
            
        if not hasattr(model, "predict_proba"):
            warnings.warn("Model doesn't support predict_proba.")
            return pd.Series(False, index=self.X.index)
        
        try:
            X_predict = self.X[feature_subset] if feature_subset is not None else self.X
            probs = model.predict_proba(X_predict)
            preds = model.classes_[probs.argmax(axis=1)]
            conf = probs.max(axis=1)
            return pd.Series((preds != self.y.values) & (conf > threshold), index=self.X.index)
        except Exception as e:
            warnings.warn(f"Label issue detection failed: {e}")
            return pd.Series(False, index=self.X.index)

    def _bias_audit(self, model, sensitive_feature, min_group_size=20, feature_subset=None):
        if sensitive_feature not in self.X.columns:
            return {"error": f"Feature '{sensitive_feature}' not found"}, 0.0
        
        if self.y is None:
            return {"error": "No labels provided"}, 0.0
            
        groups = self.X[sensitive_feature].unique()
        stats = {}
        
        for g in groups:
            idx = self.X[sensitive_feature] == g
            group_size = idx.sum()
            
            if group_size >= min_group_size:
                try:
                    y_true = self.y[idx]
                    X_predict = self.X.loc[idx, feature_subset] if feature_subset is not None else self.X[idx]
                    y_pred = model.predict(X_predict)
                    acc = accuracy_score(y_true, y_pred)
                    stats[str(g)] = {"accuracy": round(acc, 4), "sample_size": int(group_size)}
                except Exception as e:
                    stats[str(g)] = {"error": str(e)}
            else:
                stats[str(g)] = {"skipped": f"Only {group_size} samples (min: {min_group_size})"}
        
        valid_accs = [v["accuracy"] for v in stats.values() if "accuracy" in v]
        gap = round(max(valid_accs) - min(valid_accs), 4) if len(valid_accs) > 1 else 0.0
        
        return stats, gap

    def audit(self, model=None, sensitive_feature=None, noise_contamination=0.05, 
              label_threshold=0.6, check_duplicates=True, check_noise=True, 
              check_labels=True, check_bias=True, feature_subset=None):
        self._feature_subset = feature_subset
        print("Starting audit...")
        
        if check_duplicates:
            self.issues["duplicates"] = self._find_duplicates()
            print(f"   Duplicates: {self.issues['duplicates'].sum()} found")
        
        if check_noise:
            self.issues["noise"] = self._find_noise(contamination=noise_contamination)
            print(f"   Noise/Outliers: {self.issues['noise'].sum()} found")

        if check_labels and model is not None and self.y is not None:
            self.issues["label_issues"] = self._find_label_issues(model, threshold=label_threshold, feature_subset=feature_subset)
            print(f"   Label Issues: {self.issues['label_issues'].sum()} found")
        elif check_labels:
            print("   Skipping label check (requires model and labels)")

        if check_bias and model is not None and sensitive_feature is not None:
            stats, gap = self._bias_audit(model, sensitive_feature, feature_subset=feature_subset)
            self.issues["bias"] = {"stats": stats, "gap": gap}
            print(f"   Bias Audit: Max accuracy gap = {gap}")
        elif check_bias:
            print("   Skipping bias check (requires model and sensitive_feature)")

        print("Audit complete!\n")
        return self.issues

    def clean(self, remove_duplicates=True, remove_noise=True):
        if not self.issues:
            print("WARNING: No issues found. Run audit() first.")
            return

        mask = pd.Series(False, index=self.X.index)
        
        if remove_duplicates and 'duplicates' in self.issues:
            mask |= self.issues['duplicates']
        if remove_noise and 'noise' in self.issues:
            mask |= self.issues['noise']

        if mask.sum() == 0:
            print("No rows to remove.")
            return

        original_count = len(self.X)
        self.X = self.X.loc[~mask].reset_index(drop=True)
        if self.y is not None:
            self.y = self.y.loc[~mask].reset_index(drop=True)

        if "label_issues" in self.issues:
            del self.issues["label_issues"]
        if remove_duplicates and 'duplicates' in self.issues:
            del self.issues['duplicates']
        if remove_noise and 'noise' in self.issues:
            del self.issues['noise']

        self.cleaned = True
        print(f"Cleaned {mask.sum()} rows ({mask.sum()/original_count*100:.1f}%)")
        print(f"   Dataset size: {original_count} -> {len(self.X)}")

    def fix_labels(self, model, retrain=True, threshold=0.6, feature_subset=None):
        if self.y is None:
            print("WARNING: No labels to fix.")
            return 0
        
        if feature_subset is None and hasattr(self, '_feature_subset'):
            feature_subset = self._feature_subset
        
        if retrain:
            print("Retraining model on current data...")
            try:
                X_train = self.X[feature_subset] if feature_subset is not None else self.X
                model.fit(X_train, self.y)
                print("   Model retrained")
            except Exception as e:
                print(f"   WARNING: Retraining failed: {e}")
        
        if "label_issues" not in self.issues:
            print("Recalculating label issues on current data...")
            self.issues["label_issues"] = self._find_label_issues(model, threshold=threshold, feature_subset=feature_subset)
            print(f"   Found {self.issues['label_issues'].sum()} potential issues")
            
        mask = self.issues["label_issues"]
        if mask.sum() == 0:
            print("No label issues to fix.")
            return 0

        try:
            X_predict = self.X.loc[mask, feature_subset] if feature_subset is not None else self.X[mask]
            predicted_labels = model.predict(X_predict)
            self.y.loc[mask] = predicted_labels
            count = mask.sum()
            self.issues["label_issues"] = pd.Series(False, index=self.X.index)
            self.labels_fixed = True
            print(f"Fixed {count} labels ({count/len(self.y)*100:.1f}% of dataset)")
            return count
        except Exception as e:
            print(f"ERROR: Label fixing failed: {e}")
            return 0

    def restore_original(self):
        self.X = self.X_original.copy()
        self.y = self.y_original.copy() if self.y_original is not None else None
        self.issues = {}
        self.cleaned = False
        self.labels_fixed = False
        print("Dataset restored to original state")

    def report(self, path="auradata_report", report_format="html"):
        if report_format in ["html", "both"]:
            self._generate_html_report(f"{path}.html")
        if report_format in ["pdf", "both"]:
            if not PDF_AVAILABLE:
                print("WARNING: PDF generation not available.")
                print("Install with: pip install matplotlib seaborn")
            else:
                self._generate_pdf_report(f"{path}.pdf")
    
    def _generate_html_report(self, path):
        rows = []
        for k, v in self.issues.items():
            if k == "bias" and isinstance(v, dict):
                content = f"<pre>{json.dumps(v, indent=2)}</pre>"
            elif isinstance(v, pd.Series):
                count = int(v.sum())
                pct = f"{count/len(self.X)*100:.1f}%"
                content = f"{count} rows flagged ({pct})"
            else:
                content = str(v)
            rows.append(f"<tr><td style='padding:8px'><b>{k}</b></td><td style='padding:8px'>{content}</td></tr>")

        status_color = "#d4edda" if self.cleaned else "#fff3cd"
        status_text = "Cleaned" if self.cleaned else "Not Cleaned"
        
        html = f"""<html>
<head><title>AuraData Report</title>
<style>
body {{ font-family: 'Segoe UI', sans-serif; padding: 20px; background: #f5f5f5; }}
.container {{ max-width: 900px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
h1 {{ color: #333; }}
.meta {{ color: #666; margin-bottom: 20px; }}
.status {{ display: inline-block; padding: 5px 15px; border-radius: 4px; background: {status_color}; }}
table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
th {{ background-color: #f2f2f2; text-align: left; padding: 12px; font-weight: 600; }}
td {{ padding: 12px; }}
td, th {{ border: 1px solid #ddd; }}
tr:hover {{ background-color: #f9f9f9; }}
pre {{ background: #f5f5f5; padding: 10px; border-radius: 4px; }}
</style></head>
<body><div class="container">
<h1>AuraData - Data Quality Report</h1>
<div class="meta">
<p><b>Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
<p><b>Dataset Shape:</b> {self.X.shape[0]} rows x {self.X.shape[1]} features</p>
<div class="status"><b>Status:</b> {status_text}</div>
</div>
<table><tr><th>Issue Type</th><th>Details</th></tr>
{''.join(rows) if rows else '<tr><td colspan="2">No issues detected</td></tr>'}
</table></div></body></html>"""

        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"HTML report saved to {path}")
    
    def _generate_pdf_report(self, path):
        if not PDF_AVAILABLE:
            return False
        try:
            with PdfPages(path) as pdf:
                fig, ax = plt.subplots(figsize=(8.5, 11))
                ax.axis('off')
                ax.text(0.5, 0.95, 'AuraData - Data Quality Report', ha='center', va='top', fontsize=20, fontweight='bold')
                
                meta_text = f"""Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Dataset Shape: {self.X.shape[0]} rows x {self.X.shape[1]} features
Status: {'Cleaned' if self.cleaned else 'Not Cleaned'}
Labels Fixed: {'Yes' if self.labels_fixed else 'No'}"""
                ax.text(0.1, 0.85, meta_text, fontsize=11, verticalalignment='top', family='monospace',
                       bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.3))
                
                y_pos = 0.68
                ax.text(0.1, y_pos, 'Issues Detected:', fontsize=14, fontweight='bold')
                y_pos -= 0.05
                
                for k, v in self.issues.items():
                    if isinstance(v, pd.Series):
                        count = int(v.sum())
                        pct = f"{count/len(self.X)*100:.1f}%"
                        ax.text(0.1, y_pos, f"  - {k}: {count} rows ({pct})", fontsize=11, family='monospace')
                        y_pos -= 0.04
                    elif k == "bias":
                        gap = v.get('gap', 'N/A')
                        ax.text(0.1, y_pos, f"  - {k}: accuracy gap = {gap}", fontsize=11, family='monospace')
                        y_pos -= 0.04
                
                if not self.issues:
                    ax.text(0.1, y_pos, '  No issues detected', fontsize=11, family='monospace', style='italic')
                
                pdf.savefig(fig, bbox_inches='tight')
                plt.close()
                
                if any(isinstance(v, pd.Series) and v.sum() > 0 for v in self.issues.values()):
                    fig = plt.figure(figsize=(8.5, 11))
                    gs = fig.add_gridspec(3, 2, hspace=0.4, wspace=0.3, left=0.1, right=0.9, top=0.95, bottom=0.05)
                    fig.suptitle('Issue Distribution', fontsize=16, fontweight='bold')
                    
                    issue_types = []
                    issue_counts = []
                    for k, v in self.issues.items():
                        if isinstance(v, pd.Series) and v.sum() > 0:
                            issue_types.append(k)
                            issue_counts.append(int(v.sum()))
                    
                    if issue_types:
                        ax1 = fig.add_subplot(gs[0, :])
                        colors = sns.color_palette("husl", len(issue_types))
                        bars = ax1.bar(issue_types, issue_counts, color=colors, alpha=0.7, edgecolor='black')
                        ax1.set_ylabel('Count', fontsize=11)
                        ax1.set_title('Number of Issues by Type', fontsize=13, fontweight='bold')
                        ax1.grid(axis='y', alpha=0.3)
                        for bar in bars:
                            height = bar.get_height()
                            ax1.text(bar.get_x() + bar.get_width()/2., height, f'{int(height)}',
                                   ha='center', va='bottom', fontsize=10)
                        
                        ax2 = fig.add_subplot(gs[1, 0])
                        ax2.pie(issue_counts, labels=issue_types, autopct='%1.1f%%', colors=colors, startangle=90)
                        ax2.set_title('Issue Proportion', fontsize=12, fontweight='bold')
                        
                        ax3 = fig.add_subplot(gs[1, 1])
                        total_issues = sum(issue_counts)
                        clean_rows = len(self.X) - total_issues
                        ax3.pie([clean_rows, total_issues], labels=['Clean Data', 'Flagged Issues'],
                               autopct='%1.1f%%', colors=['#90EE90', '#FFB6C1'], startangle=90)
                        ax3.set_title('Dataset Composition', fontsize=12, fontweight='bold')
                        
                        ax4 = fig.add_subplot(gs[2, :])
                        quality_score = (clean_rows / len(self.X)) * 100
                        ax4.barh(['Quality Score'], [quality_score], color='#4CAF50', height=0.5)
                        ax4.set_xlim(0, 100)
                        ax4.set_xlabel('Score (%)', fontsize=11)
                        ax4.set_title('Data Quality Score', fontsize=13, fontweight='bold')
                        ax4.text(quality_score + 2, 0, f'{quality_score:.1f}%', va='center', fontsize=12, fontweight='bold')
                        ax4.grid(axis='x', alpha=0.3)
                    
                    pdf.savefig(fig, bbox_inches='tight')
                    plt.close()
                
                if "bias" in self.issues:
                    fig, ax = plt.subplots(figsize=(8.5, 11))
                    ax.axis('off')
                    ax.text(0.5, 0.95, 'Bias Analysis', ha='center', va='top', fontsize=18, fontweight='bold')
                    
                    bias_data = self.issues["bias"]
                    stats = bias_data.get("stats", {})
                    gap = bias_data.get("gap", 0.0)
                    
                    ax.text(0.1, 0.85, f'Maximum Accuracy Gap: {gap}', fontsize=13, fontweight='bold',
                           bbox=dict(boxstyle='round', facecolor='yellow' if gap > 0.1 else 'lightgreen', alpha=0.3))
                    
                    y_pos = 0.75
                    ax.text(0.1, y_pos, 'Group Performance:', fontsize=12, fontweight='bold')
                    y_pos -= 0.05
                    
                    for group, stat in stats.items():
                        if isinstance(stat, dict) and "accuracy" in stat:
                            acc = stat["accuracy"]
                            size = stat["sample_size"]
                            ax.text(0.1, y_pos, f"  {group}: Accuracy = {acc:.4f} (n={size})",
                                   fontsize=10, family='monospace')
                            y_pos -= 0.04
                    
                    groups_with_acc = [(g, s["accuracy"]) for g, s in stats.items() if isinstance(s, dict) and "accuracy" in s]
                    if groups_with_acc:
                        groups, accuracies = zip(*groups_with_acc)
                        fig2 = plt.figure(figsize=(8.5, 5))
                        ax_bar = fig2.add_subplot(111)
                        bars = ax_bar.bar(groups, accuracies, color=sns.color_palette("Set2", len(groups)),
                                         alpha=0.7, edgecolor='black')
                        ax_bar.set_ylabel('Accuracy', fontsize=11)
                        ax_bar.set_xlabel('Group', fontsize=11)
                        ax_bar.set_title('Model Accuracy by Group', fontsize=13, fontweight='bold')
                        ax_bar.set_ylim(0, 1.0)
                        ax_bar.grid(axis='y', alpha=0.3)
                        for bar, acc in zip(bars, accuracies):
                            ax_bar.text(bar.get_x() + bar.get_width()/2., acc + 0.02, f'{acc:.3f}',
                                      ha='center', va='bottom', fontsize=10)
                        pdf.savefig(fig2, bbox_inches='tight')
                        plt.close(fig2)
                    
                    pdf.savefig(fig, bbox_inches='tight')
                    plt.close()
                
                d = pdf.infodict()
                d['Title'] = 'AuraData Quality Report'
                d['Author'] = 'AuraData'
                d['CreationDate'] = datetime.now()
            
            print(f"PDF report saved to {path}")
            return True
        except Exception as e:
            print(f"ERROR: PDF generation failed: {e}")
            return False

    def summary(self):
        print("\n" + "="*50)
        print("DATASET SUMMARY")
        print("="*50)
        print(f"Shape: {self.X.shape[0]} rows x {self.X.shape[1]} features")
        print(f"Has labels: {'Yes' if self.y is not None else 'No'}")
        print(f"Cleaned: {'Yes' if self.cleaned else 'No'}")
        print(f"Labels fixed: {'Yes' if self.labels_fixed else 'No'}")
        print(f"\nIssues detected: {len(self.issues)}")
        for k, v in self.issues.items():
            if isinstance(v, pd.Series):
                print(f"  - {k}: {v.sum()}")
            elif k == "bias":
                print(f"  - {k}: gap={v.get('gap', 'N/A')}")
        print("="*50 + "\n")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("AuraData Demo - Correct Workflow")
    print("="*60 + "\n")
    
    np.random.seed(42)
    n_samples = 100
    X = pd.DataFrame(np.random.rand(n_samples, 5), columns=[f"feature_{i}" for i in range(5)])
    y = np.random.randint(0, 2, n_samples)
    X['gender'] = np.random.choice(['M', 'F'], n_samples)
    
    X.iloc[1] = X.iloc[0]
    y[1] = y[0]
    X.iloc[5, :5] = 100.0
    y[10] = 1 - y[10]
    y[20] = 1 - y[20]
    y[30] = 1 - y[30]
    
    print("Generated dataset with injected issues:\n")
    print(f"   - 1 duplicate row")
    print(f"   - 1 outlier")
    print(f"   - 3 flipped labels\n")
    
    ds = Dataset(X, y)
    
    print("STEP 1: Initial Audit (Pre-cleaning)")
    print("-" * 60)
    ds.audit(check_labels=False, check_bias=False, noise_contamination=0.05)
    
    print("\nSTEP 2: Clean Dataset")
    print("-" * 60)
    ds.clean(remove_duplicates=True, remove_noise=True)
    
    print("\nSTEP 3: Train Model on Clean Data")
    print("-" * 60)
    numeric_features = [col for col in ds.X.columns if col != 'gender']
    model = LogisticRegression(random_state=42, max_iter=1000)
    model.fit(ds.X[numeric_features], ds.y)
    print("Model trained successfully\n")
    
    print("STEP 4: Full Audit (Post-cleaning)")
    print("-" * 60)
    ds.audit(model=model, sensitive_feature='gender', label_threshold=0.7,
             check_duplicates=False, check_noise=False, feature_subset=numeric_features)
    
    print("\nSTEP 5: Fix Label Issues")
    print("-" * 60)
    ds.fix_labels(model, retrain=True, threshold=0.7, feature_subset=numeric_features)
    
    print("\nSTEP 6: Generate Report")
    print("-" * 60)
    ds.report("auradata_report", report_format="both")
    
    ds.summary()
    
    print("\nDemo complete! Check 'auradata_report.html' and 'auradata_report.pdf' for full reports.\n")