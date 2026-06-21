# ============================================
# Financial Data Analysis Dashboard
# Author: Muhammad Sohaib Imran
# FAST-NUCES, Lahore | FinTech
# Install: pip install pandas numpy matplotlib
# ============================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')


class DataAnalyzer:
    """Financial data analysis and visualization."""

    def __init__(self):
        self.data = None
        self.filename = None

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self):
        print("\n" + "=" * 60)
        print("        📊 FINANCIAL DATA ANALYSIS DASHBOARD")
        print("        Muhammad Sohaib Imran | FAST-NUCES Lahore")
        print("        Powered by Pandas, NumPy & Matplotlib")
        print("=" * 60)

    def load_data(self):
        """Load CSV file."""
        print("\n  📁 Loading Data")
        print("  " + "-" * 40)
        
        # Create sample data if no files exist
        sample_files = self.create_sample_data()
        
        print("  Available files:")
        for i, f in enumerate(sample_files, 1):
            print(f"  {i}. {f}")

        choice = input("\n  Select file (1-3) or enter filename: ").strip()
        
        try:
            if choice in ['1', '2', '3']:
                self.filename = sample_files[int(choice)-1]
            else:
                self.filename = choice
            
            self.data = pd.read_csv(self.filename)
            print(f"\n  ✅ Loaded: {self.filename}")
            print(f"  📊 Rows: {len(self.data)} | Columns: {len(self.data.columns)}")
            return True
        except FileNotFoundError:
            print(f"\n  ❌ File not found!")
            return False

    def create_sample_data(self):
        """Create sample financial datasets."""
        
        # Sample 1: Crypto prices
        dates = pd.date_range('2024-01-01', periods=30)
        crypto_data = pd.DataFrame({
            'Date': dates,
            'Bitcoin': np.random.normal(45000, 2000, 30),
            'Ethereum': np.random.normal(2500, 150, 30),
            'Solana': np.random.normal(100, 8, 30),
            'Cardano': np.random.normal(0.7, 0.05, 30)
        })
        crypto_data.to_csv('crypto_prices.csv', index=False)

        # Sample 2: Stock prices
        stock_data = pd.DataFrame({
            'Date': dates,
            'AAPL': np.random.normal(150, 5, 30),
            'GOOGL': np.random.normal(140, 6, 30),
            'MSFT': np.random.normal(380, 10, 30),
            'TSLA': np.random.normal(240, 15, 30)
        })
        stock_data.to_csv('stock_prices.csv', index=False)

        # Sample 3: Portfolio
        portfolio_data = pd.DataFrame({
            'Asset': ['Bitcoin', 'Ethereum', 'AAPL', 'GOOGL', 'Gold', 'Cash'],
            'Holdings': [0.5, 2.0, 10, 5, 100, 10000],
            'Price': [45000, 2500, 150, 140, 2000, 1],
            'Purchase_Price': [42000, 2300, 145, 135, 1950, 1],
            'Date_Purchased': ['2023-06-01', '2023-07-15', '2023-08-20', 
                              '2023-09-10', '2023-10-01', '2024-01-01']
        })
        portfolio_data.to_csv('portfolio.csv', index=False)

        return ['crypto_prices.csv', 'stock_prices.csv', 'portfolio.csv']

    def basic_stats(self):
        """Display basic statistics."""
        print("\n  📈 BASIC STATISTICS")
        print("  " + "=" * 55)
        
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        
        stats_df = self.data[numeric_cols].describe().round(4)
        print("\n" + str(stats_df))
        
        print("\n  ADDITIONAL METRICS")
        print("  " + "-" * 55)
        for col in numeric_cols:
            data = self.data[col].dropna()
            skewness = data.skew()
            kurtosis = data.kurtosis()
            cv = (data.std() / data.mean() * 100) if data.mean() != 0 else 0
            
            print(f"\n  {col}:")
            print(f"    Skewness    : {skewness:.4f} {'(Right-skewed)' if skewness > 0 else '(Left-skewed)'}")
            print(f"    Kurtosis    : {kurtosis:.4f}")
            print(f"    Coef. Var.  : {cv:.2f}%")

    def correlation_matrix(self):
        """Display correlation matrix."""
        print("\n  🔗 CORRELATION MATRIX")
        print("  " + "=" * 55)
        
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        corr = self.data[numeric_cols].corr().round(4)
        print("\n" + str(corr))
        
        print("\n  🔥 HIGHEST CORRELATIONS:")
        pairs = []
        for i in range(len(corr.columns)):
            for j in range(i+1, len(corr.columns)):
                pairs.append((corr.columns[i], corr.columns[j], corr.iloc[i,j]))
        
        pairs.sort(key=lambda x: abs(x[2]), reverse=True)
        for col1, col2, corr_val in pairs[:5]:
            icon = "🔴" if corr_val > 0.7 else "🟡" if corr_val > 0.3 else "🟢"
            print(f"  {icon} {col1} ↔ {col2}: {corr_val:.4f}")

    def price_trends(self):
        """Analyze price trends."""
        print("\n  📈 PRICE TREND ANALYSIS")
        print("  " + "=" * 55)
        
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols[:5]:
            if col in self.data.columns:
                data = self.data[col].dropna()
                if len(data) > 1:
                    pct_change = ((data.iloc[-1] - data.iloc[0]) / data.iloc[0] * 100)
                    direction = "📈 UP" if pct_change > 0 else "📉 DOWN"
                    
                    print(f"\n  {col}:")
                    print(f"    Start     : {data.iloc[0]:,.4f}")
                    print(f"    End       : {data.iloc[-1]:,.4f}")
                    print(f"    Change    : {pct_change:.2f}% {direction}")
                    print(f"    Min       : {data.min():,.4f}")
                    print(f"    Max       : {data.max():,.4f}")
                    print(f"    Volatility: {data.std():,.4f}")

    def portfolio_analysis(self):
        """Analyze investment portfolio."""
        if 'Holdings' not in self.data.columns or 'Price' not in self.data.columns:
            print("\n  ⚠️  Portfolio analysis requires 'Holdings' and 'Price' columns")
            return
        
        print("\n  💼 PORTFOLIO ANALYSIS")
        print("  " + "=" * 55)
        
        self.data['Current_Value'] = self.data['Holdings'] * self.data['Price']
        self.data['Cost_Basis'] = self.data['Holdings'] * self.data['Purchase_Price']
        self.data['Gain_Loss'] = self.data['Current_Value'] - self.data['Cost_Basis']
        self.data['Return_%'] = (self.data['Gain_Loss'] / self.data['Cost_Basis'] * 100).round(2)
        
        total_value = self.data['Current_Value'].sum()
        total_cost = self.data['Cost_Basis'].sum()
        total_gain = self.data['Gain_Loss'].sum()
        total_return = (total_gain / total_cost * 100)
        
        print(f"\n  Total Portfolio Value : Rs.{total_value:,.2f}")
        print(f"  Total Cost Basis      : Rs.{total_cost:,.2f}")
        print(f"  Total Gain/Loss       : Rs.{total_gain:,.2f}")
        print(f"  Overall Return        : {total_return:.2f}%")
        
        print(f"\n  {'Asset':<15} {'Holdings':<15} {'Price':<12} {'Value':<15} {'Return%':<10}")
        print("  " + "-" * 65)
        
        for idx, row in self.data.iterrows():
            print(f"  {row['Asset']:<15} {row['Holdings']:<15.2f} "
                  f"Rs.{row['Price']:<10.2f} Rs.{row['Current_Value']:<13.2f} "
                  f"{row['Return_%']:.2f}%")

    def risk_metrics(self):
        """Calculate risk metrics."""
        print("\n  ⚠️  RISK METRICS")
        print("  " + "=" * 55)
        
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols[:3]:
            data = self.data[col].dropna()
            if len(data) > 1:
                returns = data.pct_change().dropna()
                
                # Value at Risk (95%)
                var_95 = np.percentile(returns, 5)
                
                # Conditional Value at Risk
                cvar = returns[returns <= var_95].mean()
                
                # Sharpe Ratio (assuming 0% risk-free rate)
                sharpe = (returns.mean() / returns.std()) if returns.std() != 0 else 0
                
                print(f"\n  {col}:")
                print(f"    Daily Return (avg)    : {returns.mean()*100:.4f}%")
                print(f"    Volatility (std dev)  : {returns.std()*100:.4f}%")
                print(f"    Value at Risk (95%)   : {var_95*100:.4f}%")
                print(f"    CVaR (Expected Loss)  : {cvar*100:.4f}%")
                print(f"    Sharpe Ratio          : {sharpe:.4f}")

    def visualize_data(self):
        """Create visualizations."""
        print("\n  📊 GENERATING VISUALIZATIONS...")
        
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numeric_cols) == 0:
            print("  ⚠️  No numeric columns to visualize!")
            return
        
        fig = plt.figure(figsize=(16, 12))
        fig.patch.set_facecolor('#0f0f0f')
        
        # 1. Time series
        ax1 = plt.subplot(2, 3, 1)
        for col in numeric_cols[:4]:
            ax1.plot(self.data[col], label=col, linewidth=2, marker='o')
        ax1.set_title('Price Trends', fontsize=14, fontweight='bold', color='white')
        ax1.set_xlabel('Days', color='white')
        ax1.set_ylabel('Price', color='white')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        ax1.set_facecolor('#1a1a1a')
        ax1.tick_params(colors='white')
        
        # 2. Correlation heatmap
        ax2 = plt.subplot(2, 3, 2)
        corr = self.data[numeric_cols].corr()
        im = ax2.imshow(corr, cmap='coolwarm', aspect='auto')
        ax2.set_xticks(range(len(corr.columns)))
        ax2.set_yticks(range(len(corr.columns)))
        ax2.set_xticklabels(corr.columns, rotation=45, ha='right', color='white')
        ax2.set_yticklabels(corr.columns, color='white')
        ax2.set_title('Correlation Matrix', fontsize=14, fontweight='bold', color='white')
        plt.colorbar(im, ax=ax2)
        
        # 3. Distribution
        ax3 = plt.subplot(2, 3, 3)
        data_to_plot = [self.data[col].dropna() for col in numeric_cols[:4]]
        bp = ax3.boxplot(data_to_plot, labels=numeric_cols[:4], patch_artist=True)
        for patch in bp['boxes']:
            patch.set_facecolor('#2A9D8F')
        ax3.set_title('Distribution (Box Plot)', fontsize=14, fontweight='bold', color='white')
        ax3.set_ylabel('Price', color='white')
        ax3.set_facecolor('#1a1a1a')
        ax3.tick_params(colors='white')
        plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # 4. Returns histogram
        ax4 = plt.subplot(2, 3, 4)
        first_col = numeric_cols[0]
        returns = self.data[first_col].pct_change().dropna() * 100
        ax4.hist(returns, bins=20, color='#00ffe7', alpha=0.7, edgecolor='white')
        ax4.set_title(f'{first_col} Returns Distribution', fontsize=14, fontweight='bold', color='white')
        ax4.set_xlabel('Return %', color='white')
        ax4.set_ylabel('Frequency', color='white')
        ax4.set_facecolor('#1a1a1a')
        ax4.tick_params(colors='white')
        
        # 5. Volatility over time
        ax5 = plt.subplot(2, 3, 5)
        rolling_vol = self.data[first_col].pct_change().rolling(window=5).std() * 100
        ax5.plot(rolling_vol, color='#ff2d78', linewidth=2)
        ax5.fill_between(range(len(rolling_vol)), rolling_vol, alpha=0.3, color='#ff2d78')
        ax5.set_title('Rolling Volatility (5-day)', fontsize=14, fontweight='bold', color='white')
        ax5.set_ylabel('Volatility %', color='white')
        ax5.set_facecolor('#1a1a1a')
        ax5.tick_params(colors='white')
        
        # 6. Cumulative returns
        ax6 = plt.subplot(2, 3, 6)
        for col in numeric_cols[:4]:
            cum_returns = (1 + self.data[col].pct_change()).cumprod() * 100
            ax6.plot(cum_returns, label=col, linewidth=2)
        ax6.set_title('Cumulative Returns (Indexed to 100)', fontsize=14, fontweight='bold', color='white')
        ax6.set_xlabel('Days', color='white')
        ax6.set_ylabel('Index Value', color='white')
        ax6.legend()
        ax6.set_facecolor('#1a1a1a')
        ax6.tick_params(colors='white')
        ax6.grid(True, alpha=0.3)
        
        plt.tight_layout()
        filename = f"dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(filename, facecolor='#0f0f0f', dpi=150)
        print(f"\n  ✅ Saved: {filename}")
        plt.show()

    def export_report(self):
        """Export analysis report."""
        filename = f"analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(filename, 'w') as f:
            f.write("=" * 60 + "\n")
            f.write("FINANCIAL DATA ANALYSIS REPORT\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")
            
            f.write(f"Dataset: {self.filename}\n")
            f.write(f"Rows: {len(self.data)} | Columns: {len(self.data.columns)}\n\n")
            
            f.write("BASIC STATISTICS\n")
            f.write("-" * 60 + "\n")
            f.write(str(self.data.describe()) + "\n\n")
            
            f.write("CORRELATION MATRIX\n")
            f.write("-" * 60 + "\n")
            numeric_cols = self.data.select_dtypes(include=[np.number]).columns
            f.write(str(self.data[numeric_cols].corr()) + "\n\n")
            
            f.write("DATA OVERVIEW\n")
            f.write("-" * 60 + "\n")
            f.write(str(self.data.head(10)))
        
        print(f"\n  ✅ Report exported: {filename}")

    def main_menu(self):
        """Main menu."""
        print("\n  MENU")
        print("  " + "-" * 50)
        print("  1. 📊 Basic Statistics")
        print("  2. 🔗 Correlation Analysis")
        print("  3. 📈 Price Trends")
        print("  4. 💼 Portfolio Analysis")
        print("  5. ⚠️  Risk Metrics")
        print("  6. 📉 Visualizations")
        print("  7. 💾 Export Report")
        print("  8. 🔄 Load New Data")
        print("  0. 🚪 Exit")
        print("  " + "-" * 50)

    def run(self):
        """Main program loop."""
        self.clear_screen()
        self.print_header()
        
        if not self.load_data():
            print("\n  ❌ Failed to load data!")
            return
        
        while True:
            self.main_menu()
            choice = input("\n  Enter choice: ").strip()
            
            if choice == "1":
                self.basic_stats()
            elif choice == "2":
                self.correlation_matrix()
            elif choice == "3":
                self.price_trends()
            elif choice == "4":
                self.portfolio_analysis()
            elif choice == "5":
                self.risk_metrics()
            elif choice == "6":
                self.visualize_data()
            elif choice == "7":
                self.export_report()
            elif choice == "8":
                if self.load_data():
                    continue
            elif choice == "0":
                print("\n  📊 Thank you for using the Data Analysis Dashboard!")
                print("  — Muhammad Sohaib Imran | FAST-NUCES\n")
                break
            else:
                print("\n  ❌ Invalid choice!")
            
            input("\n  Press Enter to continue...")
            self.clear_screen()
            self.print_header()


if __name__ == "__main__":
    analyzer = DataAnalyzer()
    analyzer.run()
