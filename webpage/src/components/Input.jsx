import React, { useState, useRef } from 'react';
import pako from 'pako';

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
        
        try {
            let processedFile = file;

            // Decompress if it's a GZIP file
            if (file.name.toLowerCase().endsWith('.gz')) {
                // Read the compressed file as ArrayBuffer
                const arrayBuffer = await new Promise((resolve, reject) => {
                    const reader = new FileReader();
                    reader.onload = () => resolve(reader.result);
                    reader.onerror = reject;
                    reader.readAsArrayBuffer(file);
                });

                // Decompress using pako
                const decompressedData = pako.inflate(new Uint8Array(arrayBuffer), { to: 'string' });
                
                // Create new File object with decompressed content
                processedFile = new File(
                    [decompressedData],
                    file.name.replace(/\.gz$/i, ''),
                    { type: 'text/plain' }
                );
            }

            // Example: Submit the processed file (replace with your actual submission logic)
            const formData = new FormData();
            formData.append('file', processedFile);
            
            // Simulate API call
            console.log('Submitting file:', processedFile.name);
            // const response = await fetch('/your-api-endpoint', {
            //     method: 'POST',
            //     body: formData,
            // });
            
            // Handle successful upload
            setError('');
            alert('File processed successfully!');
            
        } catch (err) {
            setError(`Error processing file: ${err.message}`);
            console.error('Decompression error:', err);
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
                        className={`px-4 py-2 bg-green-500 text-white border-none rounded cursor-${file ? 'pointer' : 'not-allowed'}`}
                    >
                        Submit
                    </button>
                    <button 
                        onClick={handleClear}
                        disabled={!file}
                        className={`px-4 py-2 bg-red-500 text-white border-none rounded cursor-${file ? 'pointer' : 'not-allowed'}`}
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