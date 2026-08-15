enum DocumentType { pdf, image, document }

enum DocumentStatus { uploaded, processing, completed, failed }

class Document {
  final int id;
  final int ownerId;
  final String fileName;
  final String filePath;
  final DocumentType fileType;
  final int fileSize;
  final DocumentStatus status;
  final String? extractionMethod;
  final String? extractedText;
  final String? aiSummary;
  final String? aiModelUsed;
  final int processingProgress;
  final DateTime createdAt;
  final DateTime? processingStartedAt;
  final DateTime? processingCompletedAt;

  Document({
    required this.id,
    required this.ownerId,
    required this.fileName,
    required this.filePath,
    required this.fileType,
    required this.fileSize,
    required this.status,
    this.extractionMethod,
    this.extractedText,
    this.aiSummary,
    this.aiModelUsed,
    required this.processingProgress,
    required this.createdAt,
    this.processingStartedAt,
    this.processingCompletedAt,
  });

  factory Document.fromJson(Map<String, dynamic> json) {
    return Document(
      id: json['id'] as int,
      ownerId: json['owner_id'] as int,
      fileName: json['file_name'] as String,
      filePath: json['file_path'] as String,
      fileType: DocumentType.values.firstWhere(
        (e) => e.name == (json['file_type'] as String?)?.toLowerCase(),
        orElse: () => DocumentType.document,
      ),
      fileSize: json['file_size'] as int? ?? 0,
      status: DocumentStatus.values.firstWhere(
        (e) => e.name == (json['status'] as String?)?.toLowerCase(),
        orElse: () => DocumentStatus.uploaded,
      ),
      extractionMethod: json['extraction_method'] as String?,
      extractedText: json['extracted_text'] as String?,
      aiSummary: json['ai_summary'] as String?,
      aiModelUsed: json['ai_model_used'] as String?,
      processingProgress: json['processing_progress'] as int? ?? 0,
      createdAt: DateTime.parse(json['created_at'] as String),
      processingStartedAt: json['processing_started_at'] != null
          ? DateTime.parse(json['processing_started_at'] as String)
          : null,
      processingCompletedAt: json['processing_completed_at'] != null
          ? DateTime.parse(json['processing_completed_at'] as String)
          : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'owner_id': ownerId,
      'file_name': fileName,
      'file_path': filePath,
      'file_type': fileType.name,
      'file_size': fileSize,
      'status': status.name,
      'extraction_method': extractionMethod,
      'extracted_text': extractedText,
      'ai_summary': aiSummary,
      'ai_model_used': aiModelUsed,
      'processing_progress': processingProgress,
      'created_at': createdAt.toIso8601String(),
      'processing_started_at': processingStartedAt?.toIso8601String(),
      'processing_completed_at': processingCompletedAt?.toIso8601String(),
    };
  }
}
