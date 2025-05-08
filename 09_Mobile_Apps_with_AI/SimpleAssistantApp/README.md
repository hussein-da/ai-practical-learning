# React Native AI Assistant App - Conceptual Guide

This guide provides instructions for understanding the conceptual structure of the simple AI Assistant React Native app presented in this module. 

**IMPORTANT:** This directory contains only conceptual code (`App.js`, `package.json`, `.env.example`). It is **NOT** a runnable React Native project out-of-the-box. You **MUST** have a full React Native development environment set up and initialize a proper project to integrate this conceptual code.

## Goal

To create a mobile screen with:
*   An input field for the user to type text.
*   A button to send the text to an AI backend.
*   A display area to show the AI's response.

## Prerequisites

*   **React Native Environment:** Follow the official **[React Native Development Environment Setup guide](https://reactnative.dev/docs/environment-setup)** for your specific OS (macOS, Windows, Linux) and target mobile platform (iOS, Android). This is the most critical and complex step.
*   **Node.js, npm/yarn, Watchman:** Required tools for React Native development.
*   **Xcode (for iOS) / Android Studio (for Android):** Needed for simulators/emulators and native builds.
*   **Backend API Endpoint:** An accessible URL for an AI service. This could be:
    *   The Sentiment Analysis API deployed from Module 4.
    *   Directly using the OpenAI API (requires handling API key securely, potentially via a dedicated backend proxy).
    *   Another AI service endpoint.

## Conceptual Setup Steps

1.  **Initialize a React Native Project:**
    *   Once your environment is set up, use the React Native CLI to create a new project:
        ```bash
        npx react-native init MyAiAssistantApp
        cd MyAiAssistantApp
        ```
    *   This creates the full project structure including `ios` and `android` folders.

2.  **Install Dependencies:**
    *   Add necessary libraries. The conceptual `package.json` lists `react`, `react-native`. You'll likely need libraries for environment variables and potentially API calls:
        ```bash
        npm install react-native-dotenv
        # Optional: npm install axios 
        ```
    *   Follow installation steps for `react-native-dotenv` (often requires adding it to `babel.config.js`).

3.  **Replace `App.js`:**
    *   Replace the content of the default `App.js` (or `App.tsx`) file created by `npx react-native init` with the conceptual code provided in `09_Mobile_Apps_with_AI/SimpleAssistantApp/App.js`.
    *   Review the comments in the conceptual `App.js` to understand the UI components, state management, and the `handleSendRequest` function.

4.  **Configure Environment Variables:**
    *   Create a `.env` file in the root of your *actual* React Native project (`MyAiAssistantApp/`).
    *   Copy the variable from `.env.example` and set the URL for your backend AI service:
        ```env
        BACKEND_API_URL="http://your-backend-api-url/endpoint"
        # Example for Module 4 Sentiment API (if running on host port 5001):
        # BACKEND_API_URL="http://<YOUR_HOST_IP_ADDRESS>:5001/analyze_sentiment"
        # Note: Use your machine's actual IP address, not localhost, when accessing from emulator/device.
        
        # Example for OpenAI API (use a backend proxy for key security):
        # BACKEND_API_URL="https://api.openai.com/v1/chat/completions"
        # OPENAI_API_KEY="YOUR_OPENAI_API_KEY" # (Handled via proxy or secured method ideally)
        ```

5.  **Run the App:**
    *   Connect a device or start an emulator/simulator.
    *   Run the appropriate command from your project root (`MyAiAssistantApp/`):
        ```bash
        # For Android
        npx react-native run-android

        # For iOS
        npx react-native run-ios 
        ```

## Understanding the Conceptual `App.js`

*   **Imports:** Includes React, core React Native components (`View`, `Text`, `TextInput`, `Button`, `StyleSheet`), `useState`, and `react-native-dotenv`.
*   **State Variables:** Uses `useState` to manage:
    *   `inputText`: The text entered by the user.
    *   `responseText`: The response received from the AI.
    *   `isLoading`: To show a loading indicator.
*   **`handleSendRequest` Function:**
    *   This asynchronous function is triggered by the button press.
    *   Sets `isLoading` to true.
    *   Retrieves the `BACKEND_API_URL` from environment variables.
    *   Constructs the request body (e.g., `{"text": inputText}` for the sentiment API).
    *   Uses the `fetch` API (or `axios`) to send a POST request to the backend.
    *   Handles the response, extracting the relevant data (e.g., sentiment label or AI-generated text).
    *   Updates the `responseText` state.
    *   Includes basic error handling.
    *   Sets `isLoading` back to false.
*   **UI Components:** Renders the `TextInput`, `Button`, and `Text` components to display the input, trigger the request, and show the response.

## Important Considerations

*   **API Key Security:** Never embed API keys directly in mobile app code. Use a backend proxy or secure configuration method.
*   **Error Handling:** The conceptual code has basic error handling; real apps need more robust error management and user feedback.
*   **Networking on Mobile:** Ensure correct network permissions are set in `AndroidManifest.xml` (Android) and `Info.plist` (iOS).
*   **Accessing Localhost:** When running the backend API on your host machine, the mobile app (in emulator/simulator or device) needs to access your machine's local network IP address, not `localhost` or `127.0.0.1`.
*   **UI/UX:** This is a minimal UI. Real applications require significant UI/UX design. 