# Communication Protocol Specification

## Overview
This document defines the communication protocols and message formats for the cross-platform Synergy system.

## Bluetooth Communication Protocol

### Message Structure
All Bluetooth messages follow a standardized JSON format with UTF-8 encoding.

```json
{
  "message_id": "unique_uuid",
  "type": "command|response|request|notification",
  "action": "specific_action_name",
  "data": {},
  "timestamp": "2024-01-01T12:00:00Z",
  "source": "android|windows"
}
```

### Message Types

#### 1. Color Control Messages

**Color Change Command (Android → Windows)**
```json
{
  "message_id": "uuid-1234",
  "type": "command",
  "action": "color_change",
  "data": {
    "color": "RED|YELLOW|GREEN"
  },
  "timestamp": "2024-01-01T12:00:00Z",
  "source": "android"
}
```

**Color Change Response (Windows → Android)**
```json
{
  "message_id": "uuid-1234-response",
  "type": "response",
  "action": "color_change_ack",
  "data": {
    "success": true,
    "current_color": "RED",
    "error_message": null
  },
  "timestamp": "2024-01-01T12:00:01Z",
  "source": "windows"
}
```

#### 2. Wi-Fi Hotspot Information

**Hotspot Info Notification (Android → Windows)**
```json
{
  "message_id": "uuid-5678",
  "type": "notification",
  "action": "wifi_hotspot_info",
  "data": {
    "ssid": "SynergyDemo",
    "password": "synergy123",
    "ip_address": "192.168.43.1",
    "port": 8888,
    "security_type": "WPA2"
  },
  "timestamp": "2024-01-01T12:00:00Z",
  "source": "android"
}
```

**Wi-Fi Connection Status (Windows → Android)**
```json
{
  "message_id": "uuid-5678-response",
  "type": "response",
  "action": "wifi_connection_status",
  "data": {
    "connected": true,
    "ip_address": "192.168.43.100",
    "signal_strength": -45,
    "error_message": null
  },
  "timestamp": "2024-01-01T12:00:05Z",
  "source": "windows"
}
```

#### 3. File Transfer Requests

**File Transfer Request (Android ↔ Windows)**
```json
{
  "message_id": "uuid-9999",
  "type": "request",
  "action": "file_transfer_request",
  "data": {
    "file_size": 52428800,
    "file_name": "test_file_50MB.bin",
    "transfer_direction": "android_to_windows|windows_to_android",
    "checksum_type": "SHA256",
    "compression": false
  },
  "timestamp": "2024-01-01T12:00:00Z",
  "source": "android"
}
```

**File Transfer Response**
```json
{
  "message_id": "uuid-9999-response",
  "type": "response",
  "action": "file_transfer_response",
  "data": {
    "accepted": true,
    "tcp_port": 8889,
    "ready_for_transfer": true,
    "error_message": null
  },
  "timestamp": "2024-01-01T12:00:01Z",
  "source": "windows"
}
```

## TCP File Transfer Protocol

### Connection Establishment
1. File transfer initiated via Bluetooth request/response
2. TCP server started on receiving device
3. Sender connects to receiver's IP:PORT
4. Handshake performed before data transfer

### Handshake Protocol

**Transfer Initiation**
```json
{
  "protocol_version": "1.0",
  "file_metadata": {
    "name": "test_file_50MB.bin",
    "size": 52428800,
    "checksum": "sha256_hash_here",
    "chunk_size": 1048576
  },
  "transfer_id": "uuid-transfer-1234"
}
```

**Transfer Acknowledgment**
```json
{
  "status": "ready|error",
  "message": "Ready to receive file",
  "transfer_id": "uuid-transfer-1234"
}
```

### Data Transfer Format

**Chunk Header (JSON)**
```json
{
  "chunk_id": 1,
  "chunk_size": 1048576,
  "chunk_checksum": "chunk_sha256_hash",
  "is_last_chunk": false
}
```

**Data Flow**
1. Send chunk header (JSON + newline)
2. Send chunk data (binary)
3. Wait for chunk acknowledgment
4. Repeat until complete

**Chunk Acknowledgment**
```json
{
  "chunk_id": 1,
  "status": "received|error",
  "message": "Chunk received successfully"
}
```

### Transfer Completion

**Final Status**
```json
{
  "transfer_complete": true,
  "total_chunks": 50,
  "total_bytes": 52428800,
  "transfer_time_ms": 15000,
  "average_speed_mbps": 27.96,
  "file_checksum": "final_sha256_hash",
  "checksum_verified": true
}
```

## Error Handling

### Error Message Format
```json
{
  "message_id": "uuid-error",
  "type": "response",
  "action": "error",
  "data": {
    "error_code": "E001",
    "error_type": "bluetooth_connection|wifi_connection|file_transfer|protocol",
    "error_message": "Human readable error description",
    "recovery_suggestions": ["suggestion1", "suggestion2"],
    "timestamp": "2024-01-01T12:00:00Z"
  },
  "source": "android|windows"
}
```

### Error Codes
- **E001**: Bluetooth connection failed
- **E002**: Wi-Fi hotspot creation failed
- **E003**: Wi-Fi connection failed
- **E004**: File transfer initialization failed
- **E005**: File transfer interrupted
- **E006**: Checksum verification failed
- **E007**: Invalid message format
- **E008**: Unsupported operation

## State Management

### Connection States
```json
{
  "bluetooth_state": "disconnected|connecting|connected|error",
  "wifi_state": "disabled|creating_hotspot|hotspot_active|connecting|connected|error",
  "file_transfer_state": "idle|requesting|transferring|completed|error",
  "last_activity": "2024-01-01T12:00:00Z"
}
```

### Message Sequence Example

1. **Initial Connection**
   - Windows: Bluetooth scan and connect
   - Android: Accept Bluetooth connection

2. **Wi-Fi Setup**
   - Android: Create hotspot → Send hotspot info
   - Windows: Receive info → Connect to Wi-Fi → Send status

3. **Color Control**
   - Android: Send color command
   - Windows: Update UI → Send acknowledgment

4. **File Transfer**
   - Either: Send transfer request
   - Other: Accept → Start TCP server
   - Sender: Connect → Handshake → Transfer → Verify

## Security Considerations

### Authentication
- Bluetooth pairing provides device authentication
- Message timestamps prevent replay attacks
- Unique message IDs prevent duplicate processing

### Data Integrity
- SHA256 checksums for all file transfers
- Chunk-level verification during transfer
- End-to-end file verification

### Network Security
- WPA2 encryption for Wi-Fi hotspot
- TCP connections over encrypted Wi-Fi
- No persistent storage of sensitive data

## Performance Specifications

### Message Limits
- Maximum Bluetooth message size: 512 bytes
- Maximum TCP chunk size: 1MB
- Timeout values:
  - Bluetooth message: 5 seconds
  - Wi-Fi connection: 30 seconds
  - File transfer chunk: 10 seconds

### Progress Reporting
- File transfer progress updates every 1MB or 2% completion
- Speed calculations averaged over 5-second windows
- Real-time display of transfer statistics