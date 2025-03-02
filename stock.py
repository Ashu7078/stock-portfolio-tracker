import streamlit as st
import yfinance as yf
import pandas as pd

def get_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d")
        if data.empty:
            return None
        current_price = data['Close'].iloc[-1]
        previous_close = stock.info.get('previousClose', current_price)
        change_percent = ((current_price - previous_close) / previous_close) * 100
        return {'ticker': ticker, 'price': current_price, 'change_percent': change_percent}
    except Exception as e:
        return None

def main():
    st.title("Stock Portfolio Tracker")
    
    # Initialize session state for portfolio
    if 'portfolio' not in st.session_state:
        st.session_state.portfolio = []
    
    # User input for stock ticker
    new_stock = st.text_input("Enter Stock Ticker (e.g., AAPL, TSLA):").upper()
    if st.button("Add Stock") and new_stock:
        stock_data = get_stock_data(new_stock)
        if stock_data and new_stock not in st.session_state.portfolio:
            st.session_state.portfolio.append(new_stock)
        elif new_stock in st.session_state.portfolio:
            st.warning("Stock already in portfolio!")
        else:
            st.error("Invalid stock ticker!")
    
    # Display portfolio
    if st.session_state.portfolio:
        st.subheader("Your Portfolio")
        portfolio_data = []
        for stock in st.session_state.portfolio:
            data = get_stock_data(stock)
            if data:
                portfolio_data.append(data)
        
        df = pd.DataFrame(portfolio_data)
        df['change_percent'] = df['change_percent'].map(lambda x: f"{x:.2f}%")
        st.table(df)
        
        # Remove stock option
        stock_to_remove = st.selectbox("Remove Stock", st.session_state.portfolio)
        if st.button("Remove Stock"):
            st.session_state.portfolio.remove(stock_to_remove)
            st.success(f"Removed {stock_to_remove} from portfolio.")
    else:
        st.info("No stocks in your portfolio. Add some to get started!")

if __name__ == "__main__":
    main()
