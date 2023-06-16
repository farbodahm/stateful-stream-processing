FROM node:lts

# Set the working directory to /app
WORKDIR /app

# Copy the package.json and package-lock.json files to the container
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code to the container
COPY . .

# Build the Angular application
RUN npm run build --prod

# Expose port 4200 for the application
EXPOSE 4200

# Start the application
CMD ["npm", "start"]
