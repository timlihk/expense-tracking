'use client';
import React, { useState } from 'react';
import { uploadReconciliation } from '../lib/api';

interface UploadResult {
  total_rows: number;
  successful_rows: number;
  error_rows: number;
  matches?: Array<{
    company_entry: any;
    zoho_matches: any[];
    confidence: number;
  }>;
  errors?: string[];
}

export function ReconciliationUpload() {
  const [isUploading, setIsUploading] = useState(false);
  const [result, setResult] = useState<UploadResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function handleFileUpload(event: React.ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    if (!file) return;

    if (!file.name.endsWith('.csv')) {
      setError('Please upload a CSV file');
      return;
    }

    setIsUploading(true);
    setError(null);
    setResult(null);

    try {
      const uploadResult = await uploadReconciliation(file);
      setResult(uploadResult);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsUploading(false);
    }
  }

  return (
    <div className="card p-4">
      <h2 className="text-lg font-semibold mb-4">Reconciliation Upload</h2>

      <div className="mb-4">
        <label className="block text-sm font-medium mb-2">
          Upload Company T&E Report (CSV)
        </label>
        <input
          type="file"
          accept=".csv"
          onChange={handleFileUpload}
          disabled={isUploading}
          className="block w-full text-sm text-gray-400 file:mr-4 file:py-2 file:px-4 file:rounded file:border-0 file:text-sm file:font-semibold file:bg-blue-600 file:text-white hover:file:bg-blue-700 disabled:opacity-50"
        />
      </div>

      {isUploading && (
        <div className="text-blue-400 text-sm mb-4">
          <div className="animate-pulse">Uploading and processing...</div>
        </div>
      )}

      {error && (
        <div className="bg-red-900/20 border border-red-500 rounded p-3 text-red-400 text-sm mb-4">
          {error}
        </div>
      )}

      {result && (
        <div className="space-y-4">
          <div className="grid grid-cols-3 gap-4">
            <div className="bg-green-900/20 border border-green-500 rounded p-3 text-center">
              <div className="text-green-400 text-2xl font-bold">{result.successful_rows}</div>
              <div className="text-green-300 text-sm">Processed</div>
            </div>
            <div className="bg-red-900/20 border border-red-500 rounded p-3 text-center">
              <div className="text-red-400 text-2xl font-bold">{result.error_rows}</div>
              <div className="text-red-300 text-sm">Errors</div>
            </div>
            <div className="bg-blue-900/20 border border-blue-500 rounded p-3 text-center">
              <div className="text-blue-400 text-2xl font-bold">{result.total_rows}</div>
              <div className="text-blue-300 text-sm">Total Rows</div>
            </div>
          </div>

          {result.matches && result.matches.length > 0 && (
            <div>
              <h3 className="text-md font-semibold mb-2">Potential Matches</h3>
              <div className="space-y-2 max-h-64 overflow-y-auto">
                {result.matches.map((match, index) => (
                  <div key={index} className="bg-gray-700/50 rounded p-3 border border-gray-600">
                    <div className="flex justify-between items-start mb-2">
                      <div className="text-sm">
                        <span className="font-medium">{match.company_entry.merchant}</span>
                        <span className="text-gray-400 ml-2">
                          ${match.company_entry.amount} on {match.company_entry.date}
                        </span>
                      </div>
                      <span className={`px-2 py-1 rounded text-xs ${
                        match.confidence > 0.8 ? 'bg-green-900/30 text-green-400' :
                        match.confidence > 0.6 ? 'bg-yellow-900/30 text-yellow-400' :
                        'bg-red-900/30 text-red-400'
                      }`}>
                        {Math.round(match.confidence * 100)}% match
                      </span>
                    </div>
                    <div className="text-xs text-gray-400">
                      {match.zoho_matches.length} Zoho expense(s) found
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {result.errors && result.errors.length > 0 && (
            <div>
              <h3 className="text-md font-semibold mb-2 text-red-400">Processing Errors</h3>
              <div className="bg-red-900/20 border border-red-500 rounded p-3 text-sm text-red-300 max-h-32 overflow-y-auto">
                {result.errors.map((error, index) => (
                  <div key={index}>• {error}</div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}