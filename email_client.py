import smtplib
import json
from email.message import EmailMessage
from flask import Flask, request, jsonify

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Professional Email Client</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/jodit@3.24.5/build/jodit.min.css">
    <style>
        :root {
            --primary-color: #5e72e4;
            --primary-hover: #4c63d2;
            --secondary-color: #8392ab;
            --background-color: #f4f5f7;
            --surface-color: #ffffff;
            --border-color: #e9ecef;
            --text-color: #32325d;
            --text-light: #8898aa;
            --danger-color: #f5365c;
            --success-color: #2dce89;
            --info-color: #11cdef;
            --warning-color: #fb6340;
            --shadow-sm: 0 0 .5rem rgba(0,0,0,.075);
            --shadow-md: 0 0 2rem 0 rgba(136,152,170,.15);
            --shadow-lg: 0 0 3rem rgba(0,0,0,.175);
            --font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }
        
        * {
            box-sizing: border-box;
        }
        
        body {
            font-family: var(--font-family);
            margin: 0;
            background-color: var(--background-color);
            color: var(--text-color);
            display: flex;
            flex-direction: column;
            height: 100vh;
            font-size: 14px;
            line-height: 1.6;
        }
        
        header {
            background: linear-gradient(135deg, var(--primary-color) 0%, #667eea 100%);
            box-shadow: var(--shadow-md);
            position: relative;
            z-index: 10;
        }
        
        nav {
            display: flex;
            gap: 0;
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
        }
        
        nav a {
            padding: 1.25rem 1.5rem;
            text-decoration: none;
            color: rgba(255,255,255,0.8);
            font-weight: 500;
            transition: all 0.3s ease;
            position: relative;
            font-size: 15px;
        }
        
        nav a:hover {
            color: #ffffff;
            background-color: rgba(255,255,255,0.1);
        }
        
        nav a.active {
            color: #ffffff;
        }
        
        nav a.active::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 3px;
            background-color: #ffffff;
        }
        
        main {
            flex-grow: 1;
            padding: 2.5rem 2rem;
            overflow-y: auto;
            background-color: var(--background-color);
        }
        
        .page-view {
            display: none;
            animation: fadeIn 0.3s ease-in-out;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .container {
            max-width: 1100px;
            margin: 0 auto;
        }
        
        .card {
            background-color: var(--surface-color);
            border: none;
            border-radius: 0.5rem;
            margin-bottom: 2rem;
            box-shadow: var(--shadow-sm);
            transition: box-shadow 0.3s ease;
            overflow: hidden;
        }
        
        .card:hover {
            box-shadow: var(--shadow-md);
        }
        
        .card-header {
            padding: 1.25rem 1.5rem;
            background: linear-gradient(135deg, #f5f7fa 0%, #f8f9fe 100%);
            border-bottom: 1px solid var(--border-color);
            font-size: 1.125rem;
            font-weight: 600;
            color: var(--text-color);
        }
        
        .card-body {
            padding: 2rem 1.5rem;
        }
        
        .form-group {
            margin-bottom: 1.5rem;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 600;
            color: var(--text-color);
            font-size: 0.875rem;
        }
        
        .form-control {
            display: block;
            width: 100%;
            padding: 0.75rem 1rem;
            font-size: 0.875rem;
            line-height: 1.5;
            color: var(--text-color);
            background-color: var(--surface-color);
            border: 1px solid var(--border-color);
            border-radius: 0.375rem;
            transition: all 0.2s ease;
            font-family: var(--font-family);
        }
        
        .form-control:focus {
            outline: none;
            border-color: var(--primary-color);
            box-shadow: 0 0 0 0.2rem rgba(94, 114, 228, 0.25);
        }
        
        .btn {
            display: inline-block;
            font-weight: 600;
            text-align: center;
            vertical-align: middle;
            cursor: pointer;
            border: 1px solid transparent;
            padding: 0.75rem 1.5rem;
            font-size: 0.875rem;
            border-radius: 0.375rem;
            transition: all 0.2s ease;
            text-decoration: none;
            margin-right: 0.5rem;
        }
        
        .btn:hover {
            transform: translateY(-1px);
            box-shadow: var(--shadow-sm);
        }
        
        .btn-primary {
            color: #fff;
            background-color: var(--primary-color);
            border-color: var(--primary-color);
        }
        
        .btn-primary:hover {
            background-color: var(--primary-hover);
            border-color: var(--primary-hover);
        }
        
        .btn-danger {
            color: #fff;
            background-color: var(--danger-color);
            border-color: var(--danger-color);
        }
        
        .btn-secondary {
            color: #fff;
            background-color: var(--secondary-color);
            border-color: var(--secondary-color);
        }
        
        .btn-info {
            color: #fff;
            background-color: var(--info-color);
            border-color: var(--info-color);
        }
        
        .table {
            width: 100%;
            border-collapse: collapse;
        }
        
        .table th, .table td {
            padding: 1rem;
            vertical-align: middle;
            border-bottom: 1px solid var(--border-color);
            text-align: left;
        }
        
        .table thead th {
            font-weight: 600;
            color: var(--text-light);
            text-transform: uppercase;
            font-size: 0.75rem;
            letter-spacing: 0.5px;
            border-bottom: 2px solid var(--border-color);
        }
        
        .table tbody tr:hover {
            background-color: #f8f9fe;
        }
        
        .action-buttons button {
            margin-right: 0.5rem;
        }
        
        .modal {
            display: none;
            position: fixed;
            z-index: 100000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            overflow: auto;
            background-color: rgba(0,0,0,0.5);
            backdrop-filter: blur(4px);
        }
        
        .modal-content {
            background-color: var(--surface-color);
            margin: 5% auto;
            border: none;
            width: 90%;
            max-width: 600px;
            border-radius: 0.5rem;
            box-shadow: var(--shadow-lg);
            animation: modalSlideIn 0.3s ease-out;
        }
        
        @keyframes modalSlideIn {
            from { transform: translateY(-50px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        
        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1.5rem;
            border-bottom: 1px solid var(--border-color);
            background: linear-gradient(135deg, #f5f7fa 0%, #f8f9fe 100%);
        }
        
        .modal-title {
            font-size: 1.25rem;
            font-weight: 600;
            color: var(--text-color);
        }
        
        .close-button {
            color: var(--text-light);
            font-size: 1.5rem;
            font-weight: 300;
            cursor: pointer;
            transition: color 0.2s ease;
            background: none;
            border: none;
            padding: 0;
            width: 30px;
            height: 30px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
        }
        
        .close-button:hover {
            color: var(--text-color);
            background-color: rgba(0,0,0,0.05);
        }
        
        #compose-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
            margin-bottom: 1rem;
        }
        
        #compose-grid > div:first-child {
            grid-column: 1 / -1;
        }
        
        /* Enhanced Dropzone Styles */
        .dropzone {
            border: 2px dashed #c8d6e5;
            border-radius: 0.75rem;
            padding: 3rem 2rem;
            text-align: center;
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .dropzone::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, rgba(94, 114, 228, 0.05) 0%, rgba(102, 126, 234, 0.05) 100%);
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        
        .dropzone:hover {
            border-color: var(--primary-color);
            background: linear-gradient(135deg, #eef2ff 0%, #e6ecff 100%);
        }
        
        .dropzone:hover::before {
            opacity: 1;
        }
        
        .dropzone.drag-over {
            border-color: var(--primary-color);
            background: linear-gradient(135deg, #e6ecff 0%, #dce4ff 100%);
            transform: scale(1.01);
            box-shadow: 0 10px 30px rgba(94, 114, 228, 0.15);
        }
        
        .dropzone-content {
            pointer-events: none;
            position: relative;
            z-index: 1;
        }
        
        .dropzone-icon {
            width: 80px;
            height: 80px;
            margin: 0 auto 1.5rem;
            position: relative;
        }
        
        .dropzone-icon svg {
            width: 100%;
            height: 100%;
            fill: none;
            stroke: var(--primary-color);
            stroke-width: 1.5;
            stroke-linecap: round;
            stroke-linejoin: round;
        }
        
        .dropzone-text {
            color: var(--text-color);
            font-weight: 600;
            margin-bottom: 0.5rem;
            font-size: 1.125rem;
        }
        
        .dropzone-subtext {
            color: var(--text-light);
            font-size: 0.875rem;
        }
        
        /* Enhanced File List Styles */
        .file-list {
            margin-top: 1.5rem;
            display: grid;
            gap: 0.75rem;
        }
        
        .file-item {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 1rem;
            background-color: #f8f9fa;
            border: 1px solid var(--border-color);
            border-radius: 0.5rem;
            transition: all 0.2s ease;
            position: relative;
            overflow: hidden;
        }
        
        .file-item::before {
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 4px;
            background-color: var(--primary-color);
            transform: translateX(-100%);
            transition: transform 0.2s ease;
        }
        
        .file-item:hover {
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            transform: translateY(-1px);
        }
        
        .file-item:hover::before {
            transform: translateX(0);
        }
        
        .file-item-info {
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        
        .file-icon {
            width: 48px;
            height: 48px;
            background: linear-gradient(135deg, var(--primary-color) 0%, #667eea 100%);
            color: white;
            border-radius: 0.5rem;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            box-shadow: 0 4px 12px rgba(94, 114, 228, 0.25);
        }
        
        .file-details {
            text-align: left;
        }
        
        .file-name {
            font-weight: 600;
            color: var(--text-color);
            margin-bottom: 0.25rem;
        }
        
        .file-size {
            font-size: 0.75rem;
            color: var(--text-light);
        }
        
        .file-remove {
            background: #fff;
            border: 1px solid var(--border-color);
            color: var(--danger-color);
            cursor: pointer;
            padding: 0.5rem;
            border-radius: 0.375rem;
            transition: all 0.2s ease;
            width: 36px;
            height: 36px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .file-remove:hover {
            background-color: var(--danger-color);
            color: white;
            border-color: var(--danger-color);
        }
        
        .file-remove i {
            font-size: 1rem;
        }
        
        .draft-item, .sent-item {
            padding: 1.5rem;
            border: 1px solid var(--border-color);
            border-radius: 0.5rem;
            margin-bottom: 1rem;
            cursor: pointer;
            background-color: var(--surface-color);
            transition: all 0.2s ease;
        }
        
        .draft-item:hover, .sent-item:hover {
            box-shadow: var(--shadow-sm);
            transform: translateY(-2px);
            border-color: var(--primary-color);
        }
        
        .draft-item-header, .sent-item-header {
            font-weight: 600;
            color: var(--text-color);
            margin-bottom: 0.25rem;
        }
        
        .draft-item-subject, .sent-item-subject {
            color: var(--primary-color);
            font-weight: 500;
            margin-bottom: 0.5rem;
        }
        
        .draft-item-preview, .sent-item-preview {
            font-size: 0.875rem;
            color: var(--text-light);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        
        .draft-item-date {
            font-size: 0.75rem;
            color: var(--text-light);
            margin-top: 0.5rem;
        }
        
        .sent-item-content {
            display: none;
            margin-top: 1rem;
            padding-top: 1rem;
            border-top: 1px solid var(--border-color);
        }
        
        .alert {
            padding: 1rem 1.25rem;
            margin-bottom: 1rem;
            border: 1px solid transparent;
            border-radius: 0.375rem;
            animation: slideIn 0.3s ease-out;
        }
        
        @keyframes slideIn {
            from {
                transform: translateY(-10px);
                opacity: 0;
            }
            to {
                transform: translateY(0);
                opacity: 1;
            }
        }
        
        .alert-danger {
            color: #842029;
            background-color: #f8d7da;
            border-color: #f5c2c7;
        }
        
        .alert-success {
            color: #0f5132;
            background-color: #d1e7dd;
            border-color: #badbcc;
        }
        
        /* Enhanced Editor Container */
        .editor-container {
            border: 1px solid var(--border-color);
            border-radius: 0.5rem;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.04);
        }
        
        .jodit-container:not(.jodit_inline) {
            border: none !important;
        }
        
        .jodit-workplace {
            min-height: 400px;
        }
        
        .jodit-status-bar {
            background-color: #f8f9fe;
            border-top: 1px solid var(--border-color);
        }
        
        /* Jodit Fullsize Mode Fixes */
        .jodit_fullsize_box,
        .jodit-container.jodit_fullsize {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            z-index: 100001 !important;
            background: white;
        }
        
        .jodit_fullsize_box .jodit-workplace {
            height: calc(100vh - 100px) !important;
        }
        
        .button-group {
            display: flex;
            gap: 0.5rem;
            margin-top: 1.5rem;
            flex-wrap: wrap;
        }
        
        .draft-actions {
            margin-top: 1rem;
            display: flex;
            gap: 0.5rem;
        }
        
        /* Keyboard Shortcuts Info */
        .shortcuts-info {
            margin-top: 1rem;
            padding: 0.75rem 1rem;
            background-color: #f8f9fa;
            border-radius: 0.375rem;
            font-size: 0.75rem;
            color: var(--text-light);
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        
        .shortcuts-info i {
            color: var(--primary-color);
        }
        
        .shortcut-item {
            display: inline-flex;
            align-items: center;
            gap: 0.25rem;
        }
        
        .shortcut-key {
            background-color: #fff;
            padding: 0.125rem 0.375rem;
            border-radius: 0.25rem;
            border: 1px solid var(--border-color);
            font-family: monospace;
            font-size: 0.7rem;
            font-weight: 600;
        }
        
        /* Loading Spinner */
        .spinner {
            display: inline-block;
            width: 1rem;
            height: 1rem;
            border: 2px solid rgba(255,255,255,0.3);
            border-radius: 50%;
            border-top-color: white;
            animation: spin 0.8s linear infinite;
            margin-right: 0.5rem;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        /* Responsive adjustments */
        @media (max-width: 768px) {
            #compose-grid {
                grid-template-columns: 1fr;
            }
            
            .dropzone {
                padding: 2rem 1rem;
            }
            
            .dropzone-icon {
                width: 60px;
                height: 60px;
            }
        }
    </style>
</head>
<body>
    <header>
        <nav id="main-nav">
            <a href="#server-config" class="nav-link active">Server Config</a>
            <a href="#compose" class="nav-link">Compose</a>
            <a href="#sent" class="nav-link">Sent</a>
            <a href="#drafts" class="nav-link">Drafts</a>
        </nav>
    </header>

    <main>
        <div id="server-config-view" class="page-view container" style="display: block;">
            <div class="card">
                <div class="card-header">Add Server Account</div>
                <div class="card-body">
                    <form id="server-config-form">
                        <input type="hidden" id="edit-server-id">
                        <div class="form-group">
                            <label for="server-host">Server Host Name</label>
                            <input type="text" id="server-host" class="form-control" required placeholder="smtp.gmail.com">
                        </div>
                        <div class="form-group">
                            <label for="server-port">Port</label>
                            <input type="number" id="server-port" class="form-control" required placeholder="587">
                        </div>
                        <div class="form-group">
                            <label for="auth-type">Auth Type</label>
                            <select id="auth-type" class="form-control">
                                <option value="SSL">SSL</option>
                                <option value="TLS">TLS</option>
                                <option value="STARTTLS">STARTTLS</option>
                                <option value="PLAIN TEXT">PLAIN TEXT</option>
                                <option value="NONE">NONE</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="username">Username</label>
                            <input type="text" id="username" class="form-control" placeholder="your-email@example.com">
                        </div>
                        <div class="form-group">
                            <label for="password">Password</label>
                            <input type="password" id="password" class="form-control" placeholder="••••••••">
                        </div>
                        <button type="submit" class="btn btn-primary">Save Account</button>
                    </form>
                </div>
            </div>

            <div class="card">
                <div class="card-header">Show Accounts</div>
                <div class="card-body">
                    <table class="table">
                        <thead>
                            <tr>
                                <th>Server Host Name</th>
                                <th>Username</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody id="accounts-table-body">
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <div id="compose-view" class="page-view container">
            <div class="card">
                <div class="card-header">Compose Email</div>
                <div class="card-body">
                    <form id="compose-form">
                        <input type="hidden" id="draft-id">
                        <div id="compose-grid">
                            <div class="form-group">
                                <label for="from-account">From SMTP Account</label>
                                <select id="from-account" class="form-control" required></select>
                            </div>
                            <div class="form-group">
                                <label for="from-name">From Name</label>
                                <input type="text" id="from-name" class="form-control" placeholder="John Doe">
                            </div>
                            <div class="form-group">
                                <label for="from-email">From Email (Optional)</label>
                                <input type="email" id="from-email" class="form-control" placeholder="Leave empty to use account email">
                            </div>
                        </div>
                        <div class="form-group">
                            <label for="to-address">To Address(es)</label>
                            <input type="text" id="to-address" class="form-control" required placeholder="recipient@example.com, another@example.com">
                        </div>
                        <div class="form-group">
                            <label for="cc-address">CC Address(es)</label>
                            <input type="text" id="cc-address" class="form-control" placeholder="cc@example.com">
                        </div>
                        <div class="form-group">
                            <label for="bcc-address">BCC Address(es)</label>
                            <input type="text" id="bcc-address" class="form-control" placeholder="bcc@example.com">
                        </div>
                        <div class="form-group">
                            <label for="subject">Subject</label>
                            <input type="text" id="subject" class="form-control" required placeholder="Email subject">
                        </div>
                        <div class="form-group">
                            <label for="message-body">Message</label>
                            <div class="editor-container">
                                <textarea id="message-body"></textarea>
                            </div>
                        </div>
                        <div class="form-group">
                            <label>Attachments</label>
                            <div class="dropzone" id="dropzone">
                                <div class="dropzone-content">
                                    <div class="dropzone-icon">
                                        <svg viewBox="0 0 24 24">
                                            <path d="M7.5 13.5L10.5 16.5M10.5 16.5L13.5 13.5M10.5 16.5V8.5" />
                                            <path d="M19.5 14.5C19.5 11.4624 17.0376 9 14 9C13.6916 9 13.3907 9.03113 13.1004 9.09023C12.3619 6.73646 10.1098 5 7.5 5C4.18629 5 1.5 7.68629 1.5 11C1.5 14.3137 4.18629 17 7.5 17" />
                                            <path d="M19.5 14.5C19.5 11.4624 17.0376 9 14 9C11.3902 9 9.13805 10.7365 8.39961 13.0902C8.10925 13.0311 7.80842 13 7.5 13C5.01472 13 3 15.0147 3 17.5C3 19.9853 5.01472 22 7.5 22H14C17.0376 22 19.5 19.5376 19.5 16.5V14.5Z" />
                                        </svg>
                                    </div>
                                    <div class="dropzone-text">Drop files here or click to browse</div>
                                    <div class="dropzone-subtext">Maximum file size: 25MB per file</div>
                                </div>
                                <input type="file" id="attachments" class="form-control" multiple style="display: none;">
                            </div>
                            <div id="file-list" class="file-list"></div>
                        </div>
                        <div class="button-group">
                            <button type="submit" id="send-btn" class="btn btn-primary">
                                <span id="send-btn-text">Send Email</span>
                            </button>
                            <button type="button" id="save-draft-btn" class="btn btn-info">
                                <i class="fas fa-save"></i> Save as Draft
                            </button>
                        </div>
                        <div id="send-status" class="mt-3"></div>
                        <div class="shortcuts-info">
                            <i class="fas fa-keyboard"></i>
                            <span class="shortcut-item">
                                <span class="shortcut-key">Ctrl</span> + <span class="shortcut-key">S</span> Save Draft
                            </span>
                            <span class="shortcut-item">
                                <span class="shortcut-key">Ctrl</span> + <span class="shortcut-key">Enter</span> Send Email
                            </span>
                            <span class="shortcut-item">
                                <span class="shortcut-key">F11</span> Fullscreen Editor
                            </span>
                        </div>
                    </form>
                </div>
            </div>
        </div>

        <div id="sent-view" class="page-view container">
            <div class="card">
                <div class="card-header">Sent Emails</div>
                <div class="card-body" id="sent-items-list">
                </div>
            </div>
        </div>

        <div id="drafts-view" class="page-view container">
            <div class="card">
                <div class="card-header">Draft Emails</div>
                <div class="card-body" id="draft-items-list">
                </div>
            </div>
        </div>
    </main>

    <div id="edit-server-modal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h2 class="modal-title">Edit Server Account</h2>
                <button class="close-button">&times;</button>
            </div>
            <div class="card-body">
                <form id="edit-server-form">
                    <input type="hidden" id="modal-edit-server-id">
                    <div class="form-group">
                        <label for="modal-server-host">Server Host Name</label>
                        <input type="text" id="modal-server-host" class="form-control" required>
                    </div>
                    <div class="form-group">
                        <label for="modal-server-port">Port</label>
                        <input type="number" id="modal-server-port" class="form-control" required>
                    </div>
                    <div class="form-group">
                        <label for="modal-auth-type">Auth Type</label>
                        <select id="modal-auth-type" class="form-control">
                            <option value="SSL">SSL</option>
                            <option value="TLS">TLS</option>
                            <option value="STARTTLS">STARTTLS</option>
                            <option value="PLAIN TEXT">PLAIN TEXT</option>
                            <option value="NONE">NONE</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="modal-username">Username</label>
                        <input type="text" id="modal-username" class="form-control">
                    </div>
                    <div class="form-group">
                        <label for="modal-password">Password</label>
                        <input type="password" id="modal-password" class="form-control">
                    </div>
                    <button type="submit" class="btn btn-primary">Update Account</button>
                </form>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/jodit@3.24.5/build/jodit.min.js"></script>
    <script>
        let editorInstance;
        let selectedFiles = [];
        
        document.addEventListener('DOMContentLoaded', () => {
            const App = {
                DB: {
                    get: (key) => {
                        const data = localStorage.getItem(key);
                        return data ? JSON.parse(data) : [];
                    },
                    save: (key, data) => {
                        localStorage.setItem(key, JSON.stringify(data));
                    }
                },

                formatFileSize(bytes) {
                    if (bytes === 0) return '0 B';
                    const k = 1024;
                    const sizes = ['B', 'KB', 'MB', 'GB'];
                    const i = Math.floor(Math.log(bytes) / Math.log(k));
                    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
                },

                initNavigation() {
                    const navLinks = document.querySelectorAll('.nav-link');
                    navLinks.forEach(link => {
                        link.addEventListener('click', (e) => {
                            e.preventDefault();
                            const targetId = e.target.getAttribute('href').substring(1) + '-view';
                            this.showView(targetId);
                            navLinks.forEach(l => l.classList.remove('active'));
                            e.target.classList.add('active');
                        });
                    });
                },

                showView(viewId) {
                    document.querySelectorAll('.page-view').forEach(view => {
                        view.style.display = 'none';
                    });
                    const targetView = document.getElementById(viewId);
                    if (targetView) {
                        targetView.style.display = 'block';
                        if (viewId === 'compose-view') this.initComposeView();
                        if (viewId === 'sent-view') this.renderSentItems();
                        if (viewId === 'drafts-view') this.renderDraftItems();
                    }
                },
                
                initServerConfig() {
                    const form = document.getElementById('server-config-form');
                    form.addEventListener('submit', (e) => {
                        e.preventDefault();
                        const server = {
                            id: Date.now().toString(),
                            host: document.getElementById('server-host').value,
                            port: parseInt(document.getElementById('server-port').value, 10),
                            authType: document.getElementById('auth-type').value,
                            user: document.getElementById('username').value,
                            pass: document.getElementById('password').value,
                        };
                        const servers = this.DB.get('email_client_servers');
                        servers.push(server);
                        this.DB.save('email_client_servers', servers);
                        this.renderServerTable();
                        form.reset();
                    });

                    const accountsTableBody = document.getElementById('accounts-table-body');
                    accountsTableBody.addEventListener('click', (e) => {
                        const target = e.target;
                        const serverId = target.dataset.id;
                        if (target.classList.contains('edit-btn')) {
                            this.openEditModal(serverId);
                        } else if (target.classList.contains('delete-btn')) {
                            this.deleteServer(serverId);
                        }
                    });
                    this.renderServerTable();
                },

                renderServerTable() {
                    const servers = this.DB.get('email_client_servers');
                    const tableBody = document.getElementById('accounts-table-body');
                    tableBody.innerHTML = '';
                    servers.forEach(server => {
                        const row = document.createElement('tr');
                        row.innerHTML = `
                            <td>${server.host}</td>
                            <td>${server.user}</td>
                            <td class="action-buttons">
                                <button class="btn btn-secondary edit-btn" data-id="${server.id}">Edit</button>
                                <button class="btn btn-danger delete-btn" data-id="${server.id}">Delete</button>
                            </td>
                        `;
                        tableBody.appendChild(row);
                    });
                },
                
                deleteServer(serverId) {
                    if (confirm('Are you sure you want to delete this server account?')) {
                        let servers = this.DB.get('email_client_servers');
                        servers = servers.filter(s => s.id !== serverId);
                        this.DB.save('email_client_servers', servers);
                        this.renderServerTable();
                    }
                },

                initEditModal() {
                    const modal = document.getElementById('edit-server-modal');
                    const closeBtn = modal.querySelector('.close-button');
                    const form = document.getElementById('edit-server-form');

                    closeBtn.onclick = () => modal.style.display = "none";
                    window.onclick = (event) => {
                        if (event.target == modal) {
                            modal.style.display = "none";
                        }
                    };

                    form.addEventListener('submit', (e) => {
                        e.preventDefault();
                        const serverId = document.getElementById('modal-edit-server-id').value;
                        let servers = this.DB.get('email_client_servers');
                        const serverIndex = servers.findIndex(s => s.id === serverId);

                        if (serverIndex > -1) {
                            servers[serverIndex] = {
                                id: serverId,
                                host: document.getElementById('modal-server-host').value,
                                port: parseInt(document.getElementById('modal-server-port').value, 10),
                                authType: document.getElementById('modal-auth-type').value,
                                user: document.getElementById('modal-username').value,
                                pass: document.getElementById('modal-password').value,
                            };
                            this.DB.save('email_client_servers', servers);
                            this.renderServerTable();
                            modal.style.display = "none";
                        }
                    });
                },

                openEditModal(serverId) {
                    const servers = this.DB.get('email_client_servers');
                    const server = servers.find(s => s.id === serverId);
                    if (server) {
                        document.getElementById('modal-edit-server-id').value = server.id;
                        document.getElementById('modal-server-host').value = server.host;
                        document.getElementById('modal-server-port').value = server.port;
                        document.getElementById('modal-auth-type').value = server.authType;
                        document.getElementById('modal-username').value = server.user;
                        document.getElementById('modal-password').value = server.pass;
                        document.getElementById('edit-server-modal').style.display = 'block';
                    }
                },

                initComposeView() {
                    const fromAccountSelect = document.getElementById('from-account');
                    const servers = this.DB.get('email_client_servers');
                    
                    fromAccountSelect.innerHTML = '<option value="">-- Select SMTP Account --</option>';
                    servers.forEach(server => {
                        const option = document.createElement('option');
                        option.value = server.id;
                        option.textContent = `${server.user} (${server.host})`;
                        fromAccountSelect.appendChild(option);
                    });

                    const composeForm = document.getElementById('compose-form');
                    composeForm.removeEventListener('submit', this.sendEmail);
                    composeForm.addEventListener('submit', (e) => this.sendEmail(e));
                    
                    const saveDraftBtn = document.getElementById('save-draft-btn');
                    saveDraftBtn.removeEventListener('click', this.saveDraft);
                    saveDraftBtn.addEventListener('click', () => this.saveDraft());
                },
                
                saveDraft() {
                    const draftId = document.getElementById('draft-id').value || Date.now().toString();
                    const serverId = document.getElementById('from-account').value;
                    
                    const draftData = {
                        id: draftId,
                        serverId: serverId,
                        from_name: document.getElementById('from-name').value,
                        from_email: document.getElementById('from-email').value,
                        to: document.getElementById('to-address').value,
                        cc: document.getElementById('cc-address').value,
                        bcc: document.getElementById('bcc-address').value,
                        subject: document.getElementById('subject').value,
                        body: editorInstance.value,
                        timestamp: Date.now(),
                        attachments: selectedFiles.map(f => ({filename: f.name, size: f.size}))
                    };
                    
                    let drafts = this.DB.get('email_client_drafts');
                    const existingIndex = drafts.findIndex(d => d.id === draftId);
                    
                    if (existingIndex > -1) {
                        drafts[existingIndex] = draftData;
                    } else {
                        drafts.unshift(draftData);
                    }
                    
                    this.DB.save('email_client_drafts', drafts);
                    this.displayStatus('Draft saved successfully!', 'success');
                    document.getElementById('draft-id').value = draftId;
                },
                
                loadDraft(draftId) {
                    const drafts = this.DB.get('email_client_drafts');
                    const draft = drafts.find(d => d.id === draftId);
                    
                    if (draft) {
                        document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
                        document.querySelector('[href="#compose"]').classList.add('active');
                        this.showView('compose-view');
                        
                        setTimeout(() => {
                            document.getElementById('draft-id').value = draft.id;
                            document.getElementById('from-account').value = draft.serverId || '';
                            document.getElementById('from-name').value = draft.from_name || '';
                            document.getElementById('from-email').value = draft.from_email || '';
                            document.getElementById('to-address').value = draft.to || '';
                            document.getElementById('cc-address').value = draft.cc || '';
                            document.getElementById('bcc-address').value = draft.bcc || '';
                            document.getElementById('subject').value = draft.subject || '';
                            editorInstance.value = draft.body || '';
                            
                            selectedFiles = [];
                            this.updateFileList();
                        }, 100);
                    }
                },
                
                deleteDraft(draftId) {
                    if (confirm('Are you sure you want to delete this draft?')) {
                        let drafts = this.DB.get('email_client_drafts');
                        drafts = drafts.filter(d => d.id !== draftId);
                        this.DB.save('email_client_drafts', drafts);
                        this.renderDraftItems();
                    }
                },
                
                renderDraftItems() {
                    const draftItems = this.DB.get('email_client_drafts');
                    const listContainer = document.getElementById('draft-items-list');
                    listContainer.innerHTML = '';

                    if (draftItems.length === 0) {
                        listContainer.innerHTML = '<p style="text-align: center; color: var(--text-light);">No draft emails found.</p>';
                        return;
                    }

                    draftItems.forEach(item => {
                        const itemDiv = document.createElement('div');
                        itemDiv.className = 'draft-item';
                        itemDiv.dataset.id = item.id;
                        
                        const preview = new DOMParser().parseFromString(item.body, 'text/html').body.textContent || "";

                        itemDiv.innerHTML = `
                            <div class="draft-item-header">To: ${item.to || '(No recipient)'}</div>
                            <div class="draft-item-subject">${item.subject || '(No subject)'}</div>
                            <div class="draft-item-preview">${preview.substring(0, 100)}...</div>
                            <div class="draft-item-date">Saved: ${new Date(item.timestamp).toLocaleString()}</div>
                            <div class="draft-actions">
                                <button class="btn btn-primary edit-draft-btn" data-id="${item.id}">Edit Draft</button>
                                <button class="btn btn-danger delete-draft-btn" data-id="${item.id}">Delete</button>
                            </div>
                        `;
                        
                        listContainer.appendChild(itemDiv);
                    });

                    listContainer.addEventListener('click', (e) => {
                        e.stopPropagation();
                        if (e.target.classList.contains('edit-draft-btn')) {
                            const draftId = e.target.dataset.id;
                            this.loadDraft(draftId);
                        } else if (e.target.classList.contains('delete-draft-btn')) {
                            const draftId = e.target.dataset.id;
                            this.deleteDraft(draftId);
                        } else {
                            const item = e.target.closest('.draft-item');
                            if (item && !e.target.closest('.draft-actions')) {
                                this.loadDraft(item.dataset.id);
                            }
                        }
                    });
                },
                
                async sendEmail(event) {
                    event.preventDefault();
                    const sendBtn = document.getElementById('send-btn');
                    const sendBtnText = document.getElementById('send-btn-text');
                    const sendStatus = document.getElementById('send-status');
                    sendBtn.disabled = true;
                    sendBtnText.innerHTML = '<span class="spinner"></span> Sending...';
                    sendStatus.innerHTML = '';

                    const serverId = document.getElementById('from-account').value;
                    const server = this.DB.get('email_client_servers').find(s => s.id === serverId);

                    if (!server) {
                        this.displayStatus('Please select a valid SMTP account.', 'danger');
                        sendBtn.disabled = false;
                        sendBtnText.innerHTML = 'Send Email';
                        return;
                    }

                    const formData = new FormData();
                    const emailData = {
                        server_config: server,
                        from_name: document.getElementById('from-name').value,
                        from_email: document.getElementById('from-email').value,
                        to: document.getElementById('to-address').value,
                        cc: document.getElementById('cc-address').value,
                        bcc: document.getElementById('bcc-address').value,
                        subject: document.getElementById('subject').value,
                        body: editorInstance.value,
                    };
                    
                    formData.append('email_data', JSON.stringify(emailData));

                    selectedFiles.forEach(file => {
                        formData.append('attachments', file);
                    });

                    try {
                        const response = await fetch('/api/send-mail', {
                            method: 'POST',
                            body: formData
                        });
                        const result = await response.json();

                        if (response.ok) {
                            this.displayStatus('Email sent successfully!', 'success');
                            
                            const draftId = document.getElementById('draft-id').value;
                            if (draftId) {
                                let drafts = this.DB.get('email_client_drafts');
                                drafts = drafts.filter(d => d.id !== draftId);
                                this.DB.save('email_client_drafts', drafts);
                            }
                            
                            document.getElementById('compose-form').reset();
                            document.getElementById('draft-id').value = '';
                            editorInstance.value = '';
                            selectedFiles = [];
                            this.updateFileList();
                            
                            const sentMail = {
                              ...emailData,
                                id: Date.now().toString(),
                                timestamp: Date.now(),
                                attachments: selectedFiles.map(f => ({filename: f.name, size: f.size}))
                            };
                            delete sentMail.server_config;
                            const sentItems = this.DB.get('email_client_sent_mail');
                            sentItems.unshift(sentMail);
                            this.DB.save('email_client_sent_mail', sentItems);

                        } else {
                            throw new Error(result.error || 'Unknown error occurred.');
                        }
                    } catch (error) {
                        this.displayStatus(`Failed to send email: ${error.message}`, 'danger');
                    } finally {
                        sendBtn.disabled = false;
                        sendBtnText.innerHTML = 'Send Email';
                    }
                },

                displayStatus(message, type) {
                    const sendStatus = document.getElementById('send-status');
                    sendStatus.innerHTML = `<div class="alert alert-${type}">${message}</div>`;
                    setTimeout(() => {
                        sendStatus.innerHTML = '';
                    }, 5000);
                },

                renderSentItems() {
                    const sentItems = this.DB.get('email_client_sent_mail');
                    const listContainer = document.getElementById('sent-items-list');
                    listContainer.innerHTML = '';

                    if (sentItems.length === 0) {
                        listContainer.innerHTML = '<p style="text-align: center; color: var(--text-light);">No sent emails found.</p>';
                        return;
                    }

                    sentItems.forEach(item => {
                        const itemDiv = document.createElement('div');
                        itemDiv.className = 'sent-item';
                        itemDiv.dataset.id = item.id;
                        
                        const preview = new DOMParser().parseFromString(item.body, 'text/html').body.textContent || "";
                        const displayFromEmail = item.from_email || '(Account Default)';

                        itemDiv.innerHTML = `
                            <div class="sent-item-header">To: ${item.to}</div>
                            <div class="sent-item-subject">${item.subject}</div>
                            <div class="sent-item-preview">${preview.substring(0, 100)}...</div>
                            <div class="sent-item-content">
                                <p><strong>From Name:</strong> ${item.from_name || '(No name)'}</p>
                                <p><strong>From Email:</strong> ${displayFromEmail}</p>
                                <p><strong>To:</strong> ${item.to}</p>
                                ${item.cc ? `<p><strong>CC:</strong> ${item.cc}</p>` : ''}
                                ${item.bcc ? `<p><strong>BCC:</strong> ${item.bcc}</p>` : ''}
                                <p><strong>Subject:</strong> ${item.subject}</p>
                                <p><strong>Date:</strong> ${new Date(item.timestamp).toLocaleString()}</p>
                                ${item.attachments && item.attachments.length > 0 ? `<p><strong>Attachments:</strong> ${item.attachments.map(a => a.filename).join(', ')}</p>` : ''}
                                <hr>
                                <div>${item.body}</div>
                            </div>
                        `;
                        listContainer.appendChild(itemDiv);
                    });

                    listContainer.addEventListener('click', (e) => {
                        const item = e.target.closest('.sent-item');
                        if (item) {
                            const content = item.querySelector('.sent-item-content');
                            content.style.display = content.style.display === 'block' ? 'none' : 'block';
                        }
                    });
                },

                initDragDrop() {
                    const dropzone = document.getElementById('dropzone');
                    const fileInput = document.getElementById('attachments');

                    dropzone.addEventListener('click', () => fileInput.click());

                    dropzone.addEventListener('dragover', (e) => {
                        e.preventDefault();
                        dropzone.classList.add('drag-over');
                    });

                    dropzone.addEventListener('dragleave', () => {
                        dropzone.classList.remove('drag-over');
                    });

                    dropzone.addEventListener('drop', (e) => {
                        e.preventDefault();
                        dropzone.classList.remove('drag-over');
                        this.handleFiles(e.dataTransfer.files);
                    });

                    fileInput.addEventListener('change', (e) => {
                        this.handleFiles(e.target.files);
                    });
                },

                handleFiles(files) {
                    Array.from(files).forEach(file => {
                        if (file.size > 25 * 1024 * 1024) {
                            alert(`File "${file.name}" is too large. Maximum size is 25MB.`);
                            return;
                        }
                        if (!selectedFiles.some(f => f.name === file.name)) {
                            selectedFiles.push(file);
                        }
                    });
                    this.updateFileList();
                },

                updateFileList() {
                    const fileList = document.getElementById('file-list');
                    fileList.innerHTML = '';
                    
                    selectedFiles.forEach((file, index) => {
                        const fileItem = document.createElement('div');
                        fileItem.className = 'file-item';
                        
                        const ext = file.name.split('.').pop().toUpperCase();
                        const size = this.formatFileSize(file.size);
                        
                        fileItem.innerHTML = `
                            <div class="file-item-info">
                                <div class="file-icon">${ext.substring(0, 4)}</div>
                                <div class="file-details">
                                    <div class="file-name">${file.name}</div>
                                    <div class="file-size">${size}</div>
                                </div>
                            </div>
                            <button class="file-remove" data-index="${index}">
                                <i class="fas fa-times"></i>
                            </button>
                        `;
                        
                        fileList.appendChild(fileItem);
                    });

                    fileList.addEventListener('click', (e) => {
                        const btn = e.target.closest('.file-remove');
                        if (btn) {
                            const index = parseInt(btn.dataset.index);
                            selectedFiles.splice(index, 1);
                            this.updateFileList();
                        }
                    });
                },

                initEditor() {
                    editorInstance = Jodit.make('#message-body', {
                        height: 450,
                        spellcheck: true,
                        toolbarAdaptive: false,
                        toolbarSticky: true,
                        showCharsCounter: true,
                        showWordsCounter: true,
                        showXPathInStatusbar: false,
                        buttons: [
                            'source', '|',
                            'bold', 'italic', 'underline', 'strikethrough', '|',
                            'superscript', 'subscript', '|',
                            'ul', 'ol', '|',
                            'outdent', 'indent', '|',
                            'font', 'fontsize', 'brush', 'paragraph', '|',
                            'image', 'file', 'video', 'table', 'link', '|',
                            'align', 'undo', 'redo', '|',
                            'hr', 'eraser', 'copyformat', '|',
                            'symbol', 'fullsize', 'selectall', 'print', 'preview', 'find', 'about'
                        ],
                        buttonsMD: [
                            'source', '|', 'bold', 'italic', 'underline', 'strikethrough', '|',
                            'ul', 'ol', '|', 'font', 'fontsize', '|',
                            'image', 'table', 'link', '|', 'align', '|',
                            'undo', 'redo', '|', 'hr', 'eraser', 'fullsize', 'preview'
                        ],
                        buttonsSM: [
                            'bold', 'italic', '|', 'ul', 'ol', '|',
                            'fontsize', '|', 'image', 'link', '|',
                            'source', 'fullsize', 'preview'
                        ],
                        buttonsXS: [
                            'bold', 'italic', '|', 'image', 'link', '|',
                            'source', 'fullsize'
                        ],
                        events: {
                            afterInit: function (editor) {
                                // Enable spell checking
                                editor.workplace.setAttribute('spellcheck', 'true');
                            }
                        },
                        style: {
                            font: '14px -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
                        },
                        placeholder: 'Start typing your email content here...',
                        theme: 'default',
                        allowResizeX: false,
                        allowResizeY: true,
                        minHeight: 100,
                        maxHeight: 800,
                        saveModeInCookie: false,
                        removeButtons: [],
                        disablePlugins: [],
                        extraButtons: [],
                        uploader: {
                            insertImageAsBase64URI: true
                        },
                        controls: {
                            font: {
                                list: {
                                    'Andale Mono,AndaleMono,monospace': 'Andale Mono',
                                    'Arial,Helvetica,sans-serif': 'Arial',
                                    'Arial Black,Arial Black,Gadget,sans-serif': 'Arial Black',
                                    'Book Antiqua,Book Antiqua,Palatino,serif': 'Book Antiqua',
                                    'Comic Sans MS,Comic Sans MS,cursive': 'Comic Sans MS',
                                    'Courier New,Courier New,Courier,monospace': 'Courier New',
                                    'Georgia,Georgia,serif': 'Georgia',
                                    'Helvetica,Helvetica,Arial,sans-serif': 'Helvetica',
                                    'Impact,Charcoal,sans-serif': 'Impact',
                                    'Lucida Console,Monaco,monospace': 'Lucida Console',
                                    'Lucida Sans Unicode,Lucida Grande,sans-serif': 'Lucida Sans',
                                    'Palatino,Palatino Linotype,Palatino LT STD,Book Antiqua,Georgia,serif': 'Palatino',
                                    'Tahoma,Geneva,sans-serif': 'Tahoma',
                                    'Times New Roman,Times,serif': 'Times New Roman',
                                    'Trebuchet MS,Helvetica,sans-serif': 'Trebuchet MS',
                                    'Verdana,Geneva,sans-serif': 'Verdana'
                                }
                            },
                            fontsize: {
                                list: ['8', '9', '10', '11', '12', '14', '16', '18', '20', '22', '24', '26', '28', '30', '32', '34', '36', '48', '60', '72', '96']
                            }
                        },
                        language: 'en',
                        i18n: 'en',
                        tabIndex: -1,
                        toolbar: true,
                        inline: false,
                        readonly: false,
                        disabled: false,
                        autofocus: false,
                        direction: '',
                        defaultMode: Jodit.MODE_WYSIWYG,
                        useSplitMode: false,
                        colorPickerDefaultTab: 'background',
                        imageDefaultWidth: 300,
                        disablePlugins: [],
                        enter: 'p',
                        defaultFontSizePoints: 'pt',
                        cleanHTML: {
                            timeout: 300,
                            removeEmptyElements: true,
                            fillEmptyParagraph: true,
                            replaceNBSP: true,
                            replaceOldTags: {
                                i: 'em',
                                b: 'strong'
                            }
                        },
                        addNewLine: true,
                        addNewLineOnDBLClick: true,
                        addNewLineTagsTriggers: ['table', 'iframe', 'img', 'hr'],
                        askBeforePasteHTML: false,
                        askBeforePasteFromWord: false,
                        defaultActionOnPaste: 'insert_clear_html'
                    });
                },

                initKeyboardShortcuts() {
                    document.addEventListener('keydown', (e) => {
                        // Save draft - Ctrl/Cmd + S
                        if ((e.ctrlKey || e.metaKey) && e.key === 's') {
                            e.preventDefault();
                            if (document.getElementById('compose-view').style.display !== 'none') {
                                this.saveDraft();
                            }
                        }
                        
                        // Send email - Ctrl/Cmd + Enter
                        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
                            e.preventDefault();
                            if (document.getElementById('compose-view').style.display !== 'none') {
                                const sendBtn = document.getElementById('send-btn');
                                if (!sendBtn.disabled) {
                                    sendBtn.click();
                                }
                            }
                        }
                    });
                },

                init() {
                    this.initEditor();
                    this.initNavigation();
                    this.initServerConfig();
                    this.initEditModal();
                    this.initDragDrop();
                    this.initKeyboardShortcuts();
                    this.showView('server-config-view');
                }
            };

            App.init();
        });
    </script>
</body>
</html>
"""

def send_email_smtp(config, from_name, from_email, to, cc, bcc, subject, body, attachments):
    msg = EmailMessage()
    msg['Subject'] = subject
    
    # Use provided from_email if available, otherwise use account email
    actual_from_email = from_email if from_email else config.get('user')
    
    if from_name:
        msg['From'] = f"{from_name} <{actual_from_email}>"
    else:
        msg['From'] = actual_from_email
    
    all_recipients = []
    if to: all_recipients.extend([addr.strip() for addr in to.split(',')])
    if cc: all_recipients.extend([addr.strip() for addr in cc.split(',')])
    if bcc: all_recipients.extend([addr.strip() for addr in bcc.split(',')])
    
    msg['To'] = to
    if cc: msg['Cc'] = cc

    msg.set_content("This is a fallback plain text message for an HTML email.")
    msg.add_alternative(body, subtype='html')

    for attachment in attachments:
        file_data = attachment.read()
        attachment.seek(0)
        maintype, subtype = attachment.content_type.split('/', 1)
        msg.add_attachment(file_data,
                           maintype=maintype,
                           subtype=subtype,
                           filename=attachment.filename)

    try:
        server = None
        auth_type = config.get('authType', 'TLS').upper()
        host = config.get('host')
        port = config.get('port')
        user = config.get('user')
        password = config.get('pass')

        if auth_type == 'SSL':
            server = smtplib.SMTP_SSL(host, port)
        else:
            server = smtplib.SMTP(host, port)
            if auth_type in ['TLS', 'STARTTLS']:
                server.starttls()
        
        if user:
            server.login(user, password)
            
        server.send_message(msg, from_addr=actual_from_email, to_addrs=all_recipients)
        server.quit()
        return {"success": True}
    except smtplib.SMTPAuthenticationError as e:
        return {"success": False, "error": f"Authentication failed: {e.smtp_code} {e.smtp_error.decode()}"}
    except smtplib.SMTPServerDisconnected as e:
        return {"success": False, "error": f"Server disconnected unexpectedly: {e}"}
    except smtplib.SMTPException as e:
        return {"success": False, "error": f"An SMTP error occurred: {e}"}
    except ConnectionRefusedError:
        return {"success": False, "error": f"Connection refused by the server at {host}:{port}."}
    except Exception as e:
        return {"success": False, "error": f"An unexpected error occurred: {str(e)}"}

@app.route('/')
def index():
    return HTML_TEMPLATE

@app.route('/api/send-mail', methods=['POST'])
def handle_send_mail():
    if 'email_data' not in request.form:
        return jsonify({"error": "Missing email_data"}), 400

    try:
        data = json.loads(request.form['email_data'])
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON in email_data"}), 400

    attachments = request.files.getlist('attachments')

    result = send_email_smtp(
        config=data.get('server_config'),
        from_name=data.get('from_name'),
        from_email=data.get('from_email'),
        to=data.get('to'),
        cc=data.get('cc'),
        bcc=data.get('bcc'),
        subject=data.get('subject'),
        body=data.get('body'),
        attachments=attachments
    )

    if result.get("success"):
        return jsonify({"message": "Email sent successfully!"})
    else:
        return jsonify({"error": result.get("error", "An unknown error occurred.")}), 500

if __name__ == '__main__':
    print("Starting Professional Email Client...")
    print("Navigate to http://127.0.0.1:5000 or http://localhost:5000 in your web browser.")
    app.run(host='127.0.0.1', port=5000, debug=True)
