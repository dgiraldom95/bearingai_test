## Running App
1. Copy .env file to parent directory
2. docker build -t fuelpredictor . && docker run -d -p 80:5000 --env-file .env fuelpredictor 

## OpenApi docs
Available at http://127.0.0.1/docs after running api