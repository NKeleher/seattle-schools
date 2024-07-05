set shell := ["nu", "-c"]

# Start local preview
preview:
    pixi run npm run dev

# Build static site
build:
    pixi run npm run build

# Deploy Observable project
deploy: build
    pixi run npm run deploy

# Clear the local data loader cache
ojs-clean:
    pixi run npm run clean

lab:
    pixi run jupyter lab
