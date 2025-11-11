# Stage 1: Build the React app
FROM node:18-alpine AS build

# Set the working directory
WORKDIR /app

# Copy package.json and install dependencies
COPY frontend/package.json ./
# If package-lock.json exists, it should be copied too
# COPY frontend/package-lock.json ./
RUN npm install

# Copy the rest of the frontend application code
COPY frontend/ ./

# Build the application for production
RUN npm run build

# Stage 2: Serve the application with Nginx
FROM nginx:stable-alpine

# Copy the build output from the 'build' stage
COPY --from=build /app/build /usr/share/nginx/html

# Expose port 80 to the outside world
EXPOSE 80

# Start Nginx and serve the static files
CMD ["nginx", "-g", "daemon off;"]
