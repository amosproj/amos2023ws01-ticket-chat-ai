# Stage 1: Build the Angular application
FROM node:20.9.0 as build

WORKDIR /app

# Copy the package.json and install dependencies
#COPY Frontend/package*.json ./
COPY . .
RUN npm install

# Copy the rest of the application source code into the container
#COPY Frontend/ .

# Build the Angular application
RUN npm run build --prod

# Stage 2: Serve the application with nginx
FROM nginx:alpine

# Copy the build output from the first stage
COPY --from=build /app/dist/frontend /usr/share/nginx/html

# Expose the port the app runs on
EXPOSE 4200

# Start Nginx and keep it running
CMD ["nginx", "-g", "daemon off;"]
