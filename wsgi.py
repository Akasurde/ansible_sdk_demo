from main import app
import sys
import os

if __name__ == "__main__":
    if len(sys.argv) == 1:
        sys.exit("Please specify inventory type (valid values: 'gcp_compute', 'azure')")
    inventory_type = sys.argv[1]

    app.config['inventory_type'] = inventory_type
    app.run(debug=True, host='0.0.0.0', port=8000)
else:
    inventory_type = os.environ.get('SDK_INVENTORY_TYPE', 'gcp_compute')
    app.config['inventory_type'] = inventory_type

    application = app
