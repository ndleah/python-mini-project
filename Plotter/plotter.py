import os
import sys
import pandas as pd

def load_dataset(filename: str = "tips.csv") -> pd.DataFrame:
    """Load dataset relative to script directory."""
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, filename)

    if not os.path.exists(file_path):
        print(f"Error: Dataset '{filename}' not found at '{file_path}'.")
        return None

    try:
        df = pd.read_csv(file_path)
        print(f"Successfully loaded '{filename}' ({len(df)} rows, {len(df.columns)} columns).")
        return df
    except Exception as e:
        print(f"Error reading '{filename}': {e}")
        return None

def plot_data(df: pd.DataFrame, kind: str = "line", x_col: str = None, y_col: str = None, title: str = "Data Visualization"):
    """Plot dataset columns using Matplotlib / Seaborn."""
    if df is None or df.empty:
        print("Error: Empty dataset.")
        return False

    try:
        import matplotlib.pyplot as plt
        import seaborn as sns

        fig, ax = plt.subplots(figsize=(10, 6))
        cols = df.columns.tolist()

        if not x_col and len(cols) > 0:
            x_col = cols[0]
        if not y_col and len(cols) > 1:
            y_col = cols[1]

        kind = kind.lower()
        if kind in ("line", "lines"):
            df.plot(kind="line", x=x_col, y=y_col, ax=ax)
        elif kind in ("bar", "bars"):
            df.plot(kind="bar", x=x_col, y=y_col, ax=ax)
        elif kind == "scatter":
            sns.scatterplot(data=df, x=x_col, y=y_col, ax=ax)
        elif kind in ("hist", "histogram"):
            sns.histplot(df[y_col] if y_col in df else df.iloc[:, 0], kde=True, ax=ax)
        elif kind in ("box", "boxplot"):
            sns.boxplot(data=df, ax=ax)
        else:
            df.plot(ax=ax)

        plt.title(title)
        plt.tight_layout()
        print(f"Generated {kind} plot for columns: X='{x_col}', Y='{y_col}'")

        try:
            plt.show()
        except Exception:
            pass
        return True
    except Exception as e:
        print(f"Error rendering plot: {e}")
        return False

def main():
    dataset_name = sys.argv[1] if len(sys.argv) > 1 else "tips.csv"
    plot_kind = sys.argv[2] if len(sys.argv) > 2 else "line"

    df = load_dataset(dataset_name)
    if df is not None:
        print("Dataset Head:")
        print(df.head())
        plot_data(df, kind=plot_kind, title=f"Plotter - {dataset_name}")

if __name__ == '__main__':
    main()
