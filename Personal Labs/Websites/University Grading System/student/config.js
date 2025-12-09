/**
 * Student Portal Configuration
 * Update these values with your AWS resources
 */
const CONFIG = {
    AWS_REGION: 'us-east-1',
    
    // API Gateway endpoint for student APIs
    API_ENDPOINT: 'https://YOUR_API_ID.execute-api.us-east-1.amazonaws.com/prod',
    
    // Cognito User Pool for students
    COGNITO: {
        USER_POOL_ID: 'us-east-1_XXXXXXXXX',
        CLIENT_ID: 'xxxxxxxxxxxxxxxxxxxxxxxxxx'
    },
    
    // Demo mode (set to false when backend is ready)
    DEMO_MODE: true,
    DEMO: {
        ID: 'STU001',
        PASSWORD: 'demo123'
    },

    // DynamoDB Tables
    TABLES: {
        STUDENTS: 'UniGrade-Students',
        GRADES: 'UniGrade-Grades'
    }
};
