from app import create_app

# Development
app = create_app('development')

# Or Production
# app = create_app('production')

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=5000)