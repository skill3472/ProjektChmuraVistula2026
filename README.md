# Into to cloud computing project, Vistula University 2026

Simple shared counter, that allows for incrementing a shared number together, with many users.

## Launch instructions

This app currently uses only Cosmos DB and does not require docker compose or a local database.

To run locally:

1. Build the Docker image:
	```bash
	docker build -t cloudprojektvistula_backend:latest .
	```

2. Set the required Cosmos DB environment variables:
	- `COSMOS_URL`: Your Cosmos DB endpoint URL
	- `COSMOS_KEY`: Your Cosmos DB access key
	- (Optional) `COSMOS_DB`: Database name (default: `counterdb`)
	- (Optional) `COSMOS_CONTAINER`: Container name (default: `counter`)

3. Run the container:
	```bash
	docker run -p 8000:8000 \
	  -e COSMOS_URL=... \
	  -e COSMOS_KEY=... \
	  cloudprojektvistula_backend:latest
	```

The app will be available at http://localhost:8000

Automatic deployment with GitHub Actions is configured on push to master, so this step is not required for production.
