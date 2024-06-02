from flask import Flask, request, jsonify
import yfinance as yf

app = Flask(__name__)

@app.route('/fetch_data', methods=['GET'])
def fetch_data():
    ticker = request.args.get('ticker', default='AAPL', type=str)
    period = request.args.get('period', default='5y', type=str)
    try:
        data = yf.download(ticker, period=period, interval='1d')
        if data.empty:
            return jsonify({'error': 'No data found for ticker'}), 404
        data.reset_index(inplace=True)
        data['Date'] = data['Date'].astype(str)  # Convert Date to string for JSON serialization
        data_dict = data.to_dict(orient='records')
        return jsonify(data_dict)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
