import React, { useState } from 'react';
import {
  SafeAreaView,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View,
  ActivityIndicator,
  ScrollView,
  KeyboardAvoidingView,
  Platform,
  Alert
} from 'react-native';
// Import the environment variable
// Ensure you have react-native-dotenv set up correctly (babel.config.js)
import { BACKEND_API_URL } from '@env'; 

// --- Main App Component ---
const App = () => {
  const [inputText, setInputText] = useState('');
  const [responseText, setResponseText] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // --- Function to handle API request ---
  const handleSendRequest = async () => {
    if (!inputText.trim()) {
      Alert.alert("Input Required", "Please enter some text to analyze.");
      return;
    }
    if (!BACKEND_API_URL || BACKEND_API_URL === 'YOUR_BACKEND_AI_API_ENDPOINT_HERE'){
      Alert.alert("Configuration Error", "Backend API URL is not configured in .env file.");
      return;
    }

    setIsLoading(true);
    setResponseText(''); // Clear previous response

    console.log(`Sending request to: ${BACKEND_API_URL}`);
    console.log(`Request body: ${{ text: inputText }}`)

    try {
      // ** IMPORTANT **
      // Replace this fetch call logic based on your specific backend API:
      // - If calling the Sentiment Analysis API (Module 4), the body is { "text": inputText }
      // - If calling OpenAI directly (via a proxy ideally), structure the body according to OpenAI's chat completion requirements.
      const response = await fetch(BACKEND_API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          // Add any other necessary headers, e.g., Authorization for OpenAI proxy
          // 'Authorization': `Bearer ${OPENAI_API_KEY}`, // HANDLED BY PROXY ideally
        },
        body: JSON.stringify({ text: inputText }) // Example body for Sentiment API
      });

      const responseJson = await response.json();

      if (!response.ok) {
        // Handle HTTP errors (e.g., 4xx, 5xx)
        console.error("API Error Response:", responseJson);
        throw new Error(responseJson.error || `HTTP error! status: ${response.status}`);
      }
      
      console.log("API Success Response:", responseJson);

      // ** IMPORTANT ** 
      // Extract the relevant data from the responseJson based on your API's structure.
      // Example for Sentiment Analysis API:
      const aiResponse = `Sentiment: ${responseJson.sentiment}\nScore: ${responseJson.score?.toFixed(4)}`;
      // Example for a simple OpenAI Chat Completion response (assuming proxy passes it through):
      // const aiResponse = responseJson.choices?.[0]?.message?.content || "No response content found.";
      
      setResponseText(aiResponse);

    } catch (error) {
      console.error("Error sending request:", error);
      setResponseText(`Error: ${error.message}`);
      Alert.alert("Request Failed", `Could not get response: ${error.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  // --- UI Rendering ---
  return (
    <SafeAreaView style={styles.container}>
      <KeyboardAvoidingView 
        behavior={Platform.OS === "ios" ? "padding" : "height"}
        style={styles.keyboardAvoidingContainer}
      >
        <ScrollView contentContainerStyle={styles.scrollContainer}>
          <Text style={styles.title}>Simple AI Assistant</Text>

          <View style={styles.inputContainer}>
            <TextInput
              style={styles.input}
              placeholder="Enter text here..."
              value={inputText}
              onChangeText={setInputText}
              multiline
            />
            <TouchableOpacity 
              style={[styles.button, isLoading && styles.buttonDisabled]}
              onPress={handleSendRequest} 
              disabled={isLoading}
            >
              <Text style={styles.buttonText}>Send Request</Text>
            </TouchableOpacity>
          </View>

          {isLoading && (
            <ActivityIndicator size="large" color="#007AFF" style={styles.loadingIndicator} />
          )}

          {responseText ? (
            <View style={styles.responseContainer}>
              <Text style={styles.responseTitle}>AI Response:</Text>
              <Text style={styles.responseText}>{responseText}</Text>
            </View>
          ) : null}
          
        </ScrollView>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
};

// --- Styles --- (Basic styling for demonstration)
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  keyboardAvoidingContainer: {
    flex: 1,
  },
  scrollContainer: {
    flexGrow: 1,
    padding: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
    textAlign: 'center',
    color: '#333',
  },
  inputContainer: {
    marginBottom: 20,
  },
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 8,
    padding: 15,
    marginBottom: 15,
    backgroundColor: '#fff',
    minHeight: 100,
    textAlignVertical: 'top', // For Android multiline
    fontSize: 16,
  },
  button: {
    backgroundColor: '#007AFF',
    paddingVertical: 15,
    borderRadius: 8,
    alignItems: 'center',
  },
  buttonDisabled: {
    backgroundColor: '#a0a0a0',
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  loadingIndicator: {
    marginVertical: 20,
  },
  responseContainer: {
    marginTop: 20,
    padding: 15,
    backgroundColor: '#e9e9e9',
    borderRadius: 8,
  },
  responseTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 10,
    color: '#333',
  },
  responseText: {
    fontSize: 16,
    color: '#555',
  },
});

export default App; 