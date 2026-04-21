import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    # Render sets the PORT environment variable
    port = int(os.environ.get('PORT', 5000))
    # Disable debug mode on Render (production)
    debug = os.environ.get('RENDER') is None
    app.run(debug=debug, port=port, host='0.0.0.0')
