'use client';

import React, { useState, useCallback, useEffect } from 'react';
import Image from 'next/image';

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [dragPreview, setDragPreview] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [eventLink, setEventLink] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isDragging, setIsDragging] = useState(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      processFile(selectedFile);
    }
  };

  const processFile = (selectedFile: File) => {
    if (!selectedFile.type.startsWith('image/')) {
      setError('Please select an image file');
      return;
    }
    setFile(selectedFile);
    setPreview(URL.createObjectURL(selectedFile));
    setError(null);
    setEventLink(null);
  };

  const handleDragEnter = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);

    // Show preview while dragging if it's an image
    const items = Array.from(e.dataTransfer.items);
    const imageItem = items.find(item => item.type.startsWith('image/'));
    
    if (imageItem) {
      const file = e.dataTransfer.files[0];
      if (file) {
        setDragPreview(URL.createObjectURL(file));
      }
    }
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
    // Clean up drag preview
    if (dragPreview) {
      URL.revokeObjectURL(dragPreview);
      setDragPreview(null);
    }
  }, [dragPreview]);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    // Clean up drag preview
    if (dragPreview) {
      URL.revokeObjectURL(dragPreview);
      setDragPreview(null);
    }

    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile) {
      processFile(droppedFile);
    }
  }, [dragPreview]);

  // Clean up URLs on unmount
  useEffect(() => {
    return () => {
      if (preview) URL.revokeObjectURL(preview);
      if (dragPreview) URL.revokeObjectURL(dragPreview);
    };
  }, [preview, dragPreview]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) {
      setError('Please select an image first');
      return;
    }

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/api/process-image', {
        method: 'POST',
        body: formData,
        headers: {
          'Accept': 'application/json',
        },
        mode: 'cors',
        credentials: 'same-origin'
      });

      if (!response.ok) {
        if (response.status === 0) {
          throw new Error('Network error - Please check if the backend server is running');
        }
        const errorData = await response.json().catch(() => null);
        throw new Error(
          errorData?.detail || `Server error: ${response.status} ${response.statusText}`
        );
      }

      const data = await response.json();
      if (!data.event_link) {
        throw new Error('No event link received from server');
      }
      setEventLink(data.event_link);
    } catch (err) {
      console.error('Error processing image:', err);
      setError(
        err instanceof Error 
          ? err.message 
          : 'An unexpected error occurred. Please try again.'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 text-white p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-center mb-8">
          Google Calendar Event Generator
        </h1>
        
        <div className="bg-gray-800 rounded-lg shadow-xl p-8">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-4">
              <label className="block">
                <span className="text-lg font-medium">Upload Image</span>
                <div className="mt-2">
                  <div 
                    className="flex items-center justify-center w-full"
                    onDragEnter={handleDragEnter}
                    onDragOver={handleDragOver}
                    onDragLeave={handleDragLeave}
                    onDrop={handleDrop}
                  >
                    <label 
                      className={`relative flex flex-col items-center justify-center w-full h-64 border-2 border-dashed rounded-lg cursor-pointer transition-all duration-200 overflow-hidden ${
                        isDragging 
                          ? 'border-blue-500 bg-gray-700/50' 
                          : 'border-gray-600 bg-gray-700 hover:bg-gray-600'
                      }`}
                    >
                      <div className="absolute inset-0 flex items-center justify-center">
                        {(preview || dragPreview) ? (
                          <div className="relative w-full h-full">
                            <Image
                              src={dragPreview || preview || ''}
                              alt="Preview"
                              fill
                              className="object-contain"
                            />
                            {isDragging && (
                              <div className="absolute inset-0 bg-gray-900/50 flex items-center justify-center">
                                <p className="text-white text-lg font-medium">Drop to upload</p>
                              </div>
                            )}
                          </div>
                        ) : (
                          <div className="flex flex-col items-center justify-center p-6 text-center">
                            <svg className="w-10 h-10 mb-3 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                            </svg>
                            <p className="mb-2 text-sm text-gray-400">
                              <span className="font-semibold">Click to upload</span> or drag and drop
                            </p>
                            <p className="text-xs text-gray-400">PNG, JPG, WEBP, or HEIF</p>
                          </div>
                        )}
                      </div>
                      <input
                        type="file"
                        className="hidden"
                        accept="image/*"
                        onChange={handleFileChange}
                      />
                    </label>
                  </div>
                </div>
              </label>

              <button
                type="submit"
                disabled={loading || !file}
                className={`w-full py-3 px-4 rounded-lg font-medium transition-colors ${
                  loading || !file
                    ? 'bg-gray-600 cursor-not-allowed'
                    : 'bg-blue-600 hover:bg-blue-700'
                }`}
              >
                {loading ? 'Processing...' : 'Generate Calendar Event'}
              </button>
            </div>
          </form>

          {error && (
            <div className="mt-4 p-4 bg-red-900/50 border border-red-500 rounded-lg text-red-200">
              {error}
            </div>
          )}

          {eventLink && (
            <div className="mt-4 p-4 bg-green-900/50 border border-green-500 rounded-lg">
              <p className="text-green-200 mb-2">Event created successfully!</p>
              <a
                href={eventLink}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-400 hover:text-blue-300 underline break-all"
              >
                View in Google Calendar
              </a>
            </div>
          )}
        </div>
      </div>
    </main>
  );
}
