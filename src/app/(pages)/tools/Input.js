import React, { useState, useRef } from 'react';

export default function InputFQ() {
    const [file, setFile] = useState(null);
    const [error, setError] = useState('');
    const fileInputRef = useRef(null);

    const handleFileChange = (event) => {
        const selectedFile = event.target.files[0];
        const validTypes = ['application/gzip', 'application/x-gzip', 'text/plain'];
        const validExtensions = ['.fastq', '.fastq.gz'];

        if (selectedFile) {
            const fileName = selectedFile.name.toLowerCase();
            const isValidType = validTypes.includes(selectedFile.type);
            const isValidExtension = validExtensions.some(ext => fileName.endsWith(ext));

            if (isValidType || isValidExtension) {
                setFile(selectedFile);
                setError('');
            } else {
                setFile(null);
                setError('Invalid file type. Please upload a .fastq or .fastq.gz file.');
            }
        }
    };

    const handleClear = () => {
        setFile(null);
        setError('');
        // Clear the file input value
        if (fileInputRef.current) {
            fileInputRef.current.value = '';
        }
    };

    const handleSubmit = async () => {
        if (!file) return;
    
        const formData = new FormData();
        formData.append('fastqFile', file);
    
        try {
            const response = await fetch('http://your-backend-api/process-fastq', {
                method: 'POST',
                body: formData,
            });
            
            if (!response.ok) throw new Error('Processing failed');
            
            const result = await response.json();
            console.log('Analysis Results:', result);
            // Handle results (update state to display in UI)
            
        } catch (error) {
            setError(error.message || 'Error processing file');
        }
    };

    return (
        <div>
            <div style={{ marginBottom: '1rem' }}>
                <input 
                    type="file" 
                    onChange={handleFileChange} 
                    ref={fileInputRef}
                    style={{ display: 'block', marginBottom: '0.5rem' }}
                />
                <div style={{ gap: '0.5rem', display: 'flex' }}>
                    <button 
                        onClick={handleSubmit}
                        disabled={!file}
                        style={{
                            padding: '0.5rem 1rem',
                            backgroundColor: '#4CAF50',
                            color: 'white',
                            border: 'none',
                            borderRadius: '4px',
                            cursor: file ? 'pointer' : 'not-allowed'
                        }}
                    >
                        Submit
                    </button>
                    <button 
                        onClick={handleClear}
                        disabled={!file}
                        style={{
                            padding: '0.5rem 1rem',
                            backgroundColor: '#f44336',
                            color: 'white',
                            border: 'none',
                            borderRadius: '4px',
                            cursor: file ? 'pointer' : 'not-allowed'
                        }}
                    >
                        Clear
                    </button>
                </div>
            </div>
            
            {file && <p>Selected file: {file.name}</p>}
            {error && <p style={{ color: 'red' }}>{error}</p>}
        </div>
    );
}