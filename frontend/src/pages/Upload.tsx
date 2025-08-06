import React, { useState, useEffect } from 'react';
import { 
  Upload as UploadIcon, 
  FileText, 
  Download, 
  Clock, 
  CheckCircle, 
  AlertCircle,
  Activity,
  Users,
  FileSpreadsheet,
  FileImage
} from 'lucide-react';
import { uploadAssets, uploadPdfAssets } from '../services/assets';
import { useFamily } from '../contexts/FamilyContext';

interface UploadHistory {
  id: number;
  filename: string;
  file_type: string;
  status: string;
  created_at: string;
  family_id: number;
}

export default function Upload() {
  const { selectedFamilyId } = useFamily();
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [fileType, setFileType] = useState<'csv' | 'xlsx' | 'pdf'>('csv');
  const [uploading, setUploading] = useState(false);
  const [uploadHistory, setUploadHistory] = useState<UploadHistory[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setSelectedFile(file);
      setError(null);
      setSuccess(null);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile || !selectedFamilyId) {
      setError('Selecione um arquivo e uma família');
      return;
    }

    try {
      setUploading(true);
      setError(null);
      setSuccess(null);

      console.log('Upload: Starting upload process...');
      console.log('Upload: File details:', {
        name: selectedFile.name,
        size: selectedFile.size,
        type: selectedFile.type
      });

      let result;
      if (fileType === 'pdf') {
        console.log('Upload: Uploading PDF file...');
        result = await uploadPdfAssets(selectedFile, selectedFamilyId);
      } else {
        console.log('Upload: Uploading CSV/Excel file...');
        result = await uploadAssets(selectedFile, selectedFamilyId);
      }

      console.log('Upload: Upload result:', result);
      setSuccess(`Upload realizado com sucesso! ${Array.isArray(result) ? result.length : 0} ativos importados.`);
      setSelectedFile(null);
      
      // Simular histórico de upload
      const newHistoryItem: UploadHistory = {
        id: Date.now(),
        filename: selectedFile.name,
        file_type: fileType.toUpperCase(),
        status: 'success',
        created_at: new Date().toISOString(),
        family_id: selectedFamilyId
      };
      setUploadHistory([newHistoryItem, ...uploadHistory]);
      
    } catch (err: any) {
      console.error('Upload: Error during upload:', err);
      console.error('Upload: Error response:', err.response);
      console.error('Upload: Error data:', err.response?.data);
      setError(err.response?.data?.error || 'Erro ao fazer upload do arquivo');
    } finally {
      setUploading(false);
    }
  };

  const downloadTemplate = (type: 'csv' | 'xlsx') => {
    const templateData = {
      csv: 'name,asset_type,value,acquisition_date,details\n"CDB Banco XYZ","renda_fixa",10000.00,2024-01-15,"{}"\n"Ações Petrobras","renda_variavel",5000.00,2024-01-20,"{\\"ticker\\":\\"PETR4\\"}"',
      xlsx: 'name,asset_type,value,acquisition_date,details\n"CDB Banco XYZ","renda_fixa",10000.00,2024-01-15,"{}"\n"Ações Petrobras","renda_variavel",5000.00,2024-01-20,"{\\"ticker\\":\\"PETR4\\"}"'
    };

    const blob = new Blob([templateData[type]], { type: type === 'csv' ? 'text/csv' : 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `template_ativos.${type}`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getFileTypeIcon = (type: string) => {
    switch (type.toLowerCase()) {
      case 'pdf':
        return <FileText size={16} />;
      case 'csv':
      case 'xlsx':
        return <FileSpreadsheet size={16} />;
      default:
        return <FileImage size={16} />;
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'success':
        return <CheckCircle size={16} color="#28a745" />;
      case 'error':
        return <AlertCircle size={16} color="#dc3545" />;
      case 'processing':
        return <Activity size={16} color="#ffc107" />;
      default:
        return <Clock size={16} color="#6c757d" />;
    }
  };

  if (!selectedFamilyId) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '400px',
        color: '#666'
      }}>
        <div style={{ textAlign: 'center' }}>
          <Users size={48} style={{ marginBottom: 16, opacity: 0.6 }} />
          <div>Selecione uma família para fazer upload de arquivos.</div>
        </div>
      </div>
    );
  }

  return (
    <div style={{ maxWidth: 1200, margin: '0 auto' }}>
      <div style={{ marginBottom: 32 }}>
        <h1 style={{ 
          color: '#222', 
          marginBottom: 16, 
          fontSize: '28px',
          fontWeight: 600,
          display: 'flex',
          alignItems: 'center',
          gap: 12
        }}>
          <UploadIcon size={28} />
          Upload de Arquivos
        </h1>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 32 }}>
        {/* Área de Upload */}
        <div style={{
          background: '#fff',
          borderRadius: 16,
          padding: 32,
          boxShadow: '0 4px 20px rgba(0,0,0,0.08)',
          border: '1px solid #e9ecef'
        }}>
          <h3 style={{ 
            color: '#222', 
            marginBottom: 24, 
            fontSize: 20,
            fontWeight: 600,
            display: 'flex',
            alignItems: 'center',
            gap: 8
          }}>
            <UploadIcon size={20} />
            Upload de Arquivos
          </h3>

          {/* Seleção de Tipo */}
          <div style={{ marginBottom: 24 }}>
            <label style={{ display: 'block', marginBottom: 8, color: '#666', fontSize: 14 }}>
              Tipo de Arquivo
            </label>
            <div style={{ display: 'flex', gap: 12 }}>
              {[
                { value: 'csv', label: 'CSV', icon: <FileSpreadsheet size={16} /> },
                { value: 'xlsx', label: 'Excel', icon: <FileSpreadsheet size={16} /> },
                { value: 'pdf', label: 'PDF', icon: <FileText size={16} /> }
              ].map((type) => (
                <button
                  key={type.value}
                  onClick={() => setFileType(type.value as 'csv' | 'xlsx' | 'pdf')}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: 8,
                    padding: '10px 16px',
                    borderRadius: 8,
                    border: fileType === type.value ? '2px solid #667eea' : '1px solid #ddd',
                    background: fileType === type.value ? '#f0f4ff' : '#fff',
                    color: fileType === type.value ? '#667eea' : '#666',
                    cursor: 'pointer',
                    fontSize: 14,
                    fontWeight: fileType === type.value ? 600 : 500,
                    transition: 'all 0.2s ease'
                  }}
                >
                  {type.icon}
                  {type.label}
                </button>
              ))}
            </div>
          </div>

          {/* Área de Drop */}
          <div style={{
            border: '2px dashed #ddd',
            borderRadius: 12,
            padding: 40,
            textAlign: 'center',
            background: selectedFile ? '#f0f4ff' : '#f8f9fa',
            transition: 'all 0.2s ease',
            cursor: 'pointer'
          }}
          onClick={() => document.getElementById('file-input')?.click()}
          >
            <input
              id="file-input"
              type="file"
              accept={fileType === 'pdf' ? '.pdf' : fileType === 'csv' ? '.csv' : '.xlsx,.xls'}
              onChange={handleFileSelect}
              style={{ display: 'none' }}
            />
            
            {selectedFile ? (
              <div>
                <CheckCircle size={48} color="#28a745" style={{ marginBottom: 16 }} />
                <div style={{ fontWeight: 600, color: '#222', marginBottom: 8 }}>
                  {selectedFile.name}
                </div>
                <div style={{ color: '#666', fontSize: 14 }}>
                  {formatFileSize(selectedFile.size)}
                </div>
              </div>
            ) : (
              <div>
                <UploadIcon size={48} color="#667eea" style={{ marginBottom: 16 }} />
                <div style={{ fontWeight: 600, color: '#222', marginBottom: 8 }}>
                  Clique para selecionar um arquivo
                </div>
                <div style={{ color: '#666', fontSize: 14 }}>
                  ou arraste e solte aqui
                </div>
              </div>
            )}
          </div>

          {/* Botão de Upload */}
          <button
            onClick={handleUpload}
            disabled={!selectedFile || uploading}
            style={{
              width: '100%',
              marginTop: 24,
              padding: '12px 24px',
              borderRadius: 8,
              border: 'none',
              background: selectedFile && !uploading 
                ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' 
                : '#e9ecef',
              color: selectedFile && !uploading ? 'white' : '#6c757d',
              cursor: selectedFile && !uploading ? 'pointer' : 'not-allowed',
              fontSize: 16,
              fontWeight: 600,
              transition: 'all 0.2s ease',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: 8
            }}
            onMouseEnter={(e) => {
              if (selectedFile && !uploading) {
                e.currentTarget.style.transform = 'translateY(-1px)';
                e.currentTarget.style.boxShadow = '0 4px 12px rgba(102, 126, 234, 0.3)';
              }
            }}
            onMouseLeave={(e) => {
              if (selectedFile && !uploading) {
                e.currentTarget.style.transform = 'translateY(0)';
                e.currentTarget.style.boxShadow = 'none';
              }
            }}
          >
            {uploading ? (
              <>
                <Activity size={16} style={{ 
                  transform: 'rotate(0deg)',
                  transition: 'transform 0.1s linear'
                }} />
                Processando...
              </>
            ) : (
              <>
                <UploadIcon size={16} />
                Fazer Upload
              </>
            )}
          </button>

          {/* Mensagens */}
          {error && (
            <div style={{
              marginTop: 16,
              padding: '12px 16px',
              borderRadius: 8,
              background: '#f8d7da',
              color: '#721c24',
              border: '1px solid #f5c6cb',
              display: 'flex',
              alignItems: 'center',
              gap: 8
            }}>
              <AlertCircle size={16} />
              {error}
            </div>
          )}

          {success && (
            <div style={{
              marginTop: 16,
              padding: '12px 16px',
              borderRadius: 8,
              background: '#d4edda',
              color: '#155724',
              border: '1px solid #c3e6cb',
              display: 'flex',
              alignItems: 'center',
              gap: 8
            }}>
              <CheckCircle size={16} />
              {success}
            </div>
          )}
        </div>

        {/* Templates e Histórico */}
        <div style={{ display: 'grid', gap: 24 }}>
          {/* Templates */}
          <div style={{
            background: '#fff',
            borderRadius: 16,
            padding: 24,
            boxShadow: '0 4px 20px rgba(0,0,0,0.08)',
            border: '1px solid #e9ecef'
          }}>
            <h3 style={{ 
              color: '#222', 
              marginBottom: 20, 
              fontSize: 18,
              fontWeight: 600,
              display: 'flex',
              alignItems: 'center',
              gap: 8
            }}>
              <Download size={20} />
              Templates
            </h3>
            
            <div style={{ display: 'grid', gap: 12 }}>
              <button
                onClick={() => downloadTemplate('csv')}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 8,
                  padding: '10px 16px',
                  borderRadius: 8,
                  border: '1px solid #ddd',
                  background: '#fff',
                  color: '#666',
                  cursor: 'pointer',
                  fontSize: 14,
                  transition: 'all 0.2s ease'
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.background = '#f8f9fa';
                  e.currentTarget.style.color = '#333';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.background = '#fff';
                  e.currentTarget.style.color = '#666';
                }}
              >
                <FileSpreadsheet size={16} />
                Download Template CSV
              </button>
              
              <button
                onClick={() => downloadTemplate('xlsx')}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 8,
                  padding: '10px 16px',
                  borderRadius: 8,
                  border: '1px solid #ddd',
                  background: '#fff',
                  color: '#666',
                  cursor: 'pointer',
                  fontSize: 14,
                  transition: 'all 0.2s ease'
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.background = '#f8f9fa';
                  e.currentTarget.style.color = '#333';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.background = '#fff';
                  e.currentTarget.style.color = '#666';
                }}
              >
                <FileSpreadsheet size={16} />
                Download Template Excel
              </button>
            </div>
          </div>

          {/* Histórico de Uploads */}
          <div style={{
            background: '#fff',
            borderRadius: 16,
            padding: 24,
            boxShadow: '0 4px 20px rgba(0,0,0,0.08)',
            border: '1px solid #e9ecef'
          }}>
            <h3 style={{ 
              color: '#222', 
              marginBottom: 20, 
              fontSize: 18,
              fontWeight: 600,
              display: 'flex',
              alignItems: 'center',
              gap: 8
            }}>
              <Clock size={20} />
              Histórico de Uploads
            </h3>
            
            <div style={{ display: 'grid', gap: 12 }}>
              {uploadHistory.length === 0 ? (
                <div style={{ 
                  textAlign: 'center', 
                  padding: '24px 0', 
                  color: '#666',
                  fontSize: 14
                }}>
                  Nenhum upload realizado ainda
                </div>
              ) : (
                uploadHistory.map((item) => (
                  <div key={item.id} style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: 12,
                    padding: '12px 16px',
                    background: '#f8f9fa',
                    borderRadius: 8,
                    border: '1px solid #e9ecef'
                  }}>
                    {getFileTypeIcon(item.file_type)}
                    <div style={{ flex: 1 }}>
                      <div style={{ fontWeight: 500, color: '#222', fontSize: 14 }}>
                        {item.filename}
                      </div>
                      <div style={{ color: '#666', fontSize: 12 }}>
                        {formatDate(item.created_at)}
                      </div>
                    </div>
                    {getStatusIcon(item.status)}
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
} 