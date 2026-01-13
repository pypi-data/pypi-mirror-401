"use strict";
(self["webpackChunkdeepanalyze"] = self["webpackChunkdeepanalyze"] || []).push([["style_index_js"],{

/***/ "./node_modules/css-loader/dist/cjs.js!./style/base.css":
/*!**************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./style/base.css ***!
  \**************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/sourceMaps.js */ "./node_modules/css-loader/dist/runtime/sourceMaps.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_getUrl_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/getUrl.js */ "./node_modules/css-loader/dist/runtime/getUrl.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_getUrl_js__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_getUrl_js__WEBPACK_IMPORTED_MODULE_2__);
// Imports



var ___CSS_LOADER_URL_IMPORT_0___ = new URL(/* asset import */ __webpack_require__(/*! ./logo.png */ "./style/logo.png"), __webpack_require__.b);
var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default()));
var ___CSS_LOADER_URL_REPLACEMENT_0___ = _node_modules_css_loader_dist_runtime_getUrl_js__WEBPACK_IMPORTED_MODULE_2___default()(___CSS_LOADER_URL_IMPORT_0___);
// Module
___CSS_LOADER_EXPORT___.push([module.id, `/*
    See the JupyterLab Developer Guide for useful CSS Patterns:

    https://jupyterlab.readthedocs.io/en/stable/developer/css.html
*/

.deepanalyze-chat-panel {
  /* Modern VS Code / Cursor inspired variables */
  --deepanalyze-bg: var(--jp-layout-color1);
  --deepanalyze-bg-secondary: var(--jp-layout-color2);
  --deepanalyze-border: var(--jp-border-color2);
  --deepanalyze-text: var(--jp-ui-font-color1);
  --deepanalyze-text-secondary: var(--jp-ui-font-color2);
  --deepanalyze-primary: var(--jp-brand-color1);
  --deepanalyze-primary-hover: var(--jp-brand-color0);
  --deepanalyze-primary-text: #ffffff;
  --deepanalyze-radius: 6px;
  --deepanalyze-input-bg: var(--jp-layout-color0);
  --deepanalyze-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);

  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 0;
  background: var(--deepanalyze-bg);
  color: var(--deepanalyze-text);
  font-family: var(--jp-ui-font-family);
  font-size: var(--jp-ui-font-size1);
  padding: 0; /* Remove padding to fill the tab */
}

.deepanalyze-chat-card {
  flex: 1 1 auto;
  min-height: 0;
  display: flex;
  flex-direction: column;
  border: none; /* Remove border */
  border-radius: 0; /* Remove radius */
  background: var(--deepanalyze-bg);
  overflow: hidden;
}

/* Header */
.deepanalyze-chat-panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 16px;
  border-bottom: 1px solid var(--deepanalyze-border);
  background: var(--deepanalyze-bg);
  font-size: 0.9em;
  font-weight: 600;
  color: var(--deepanalyze-text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.deepanalyze-chat-panel-title {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.deepanalyze-chat-panel-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.deepanalyze-chat-exit-button {
  border: none;
  border-radius: 4px;
  padding: 8px 16px;
  background: transparent;
  color: var(--deepanalyze-text-secondary);
  cursor: pointer;
  font-size: 1em;
  font-weight: 600;
  transition: background 0.2s, color 0.2s;
}

.deepanalyze-chat-exit-button:hover {
  background: var(--deepanalyze-bg-secondary);
  color: var(--deepanalyze-text);
}

/* Messages Area */
.deepanalyze-chat-messages {
  flex: 1 1 auto;
  min-height: 0;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 24px; /* More space between messages */
  background: var(--deepanalyze-bg);
}

.deepanalyze-chat-message {
  display: flex;
  flex-direction: column;
  gap: 6px;
  max-width: 100%;
}

.deepanalyze-chat-message-user {
  align-items: flex-end;
}

.deepanalyze-chat-message-assistant,
.deepanalyze-chat-message-system {
  align-items: flex-start;
}

.deepanalyze-chat-bubble {
  max-width: 90%;
  padding: 10px 14px;
  border-radius: var(--deepanalyze-radius);
  line-height: 1.6;
  font-size: var(--jp-ui-font-size1);
  position: relative;
}

/* User Message Style */
.deepanalyze-chat-message-user .deepanalyze-chat-bubble {
  background: var(--deepanalyze-primary);
  color: var(--deepanalyze-primary-text);
  border-bottom-right-radius: 2px;
  box-shadow: var(--deepanalyze-shadow);
}

/* Assistant Message Style */
.deepanalyze-chat-message-assistant .deepanalyze-chat-bubble {
  background: transparent;
  color: var(--deepanalyze-text);
  padding: 0; /* Remove padding for assistant to align with code blocks */
  max-width: 100%;
  width: 100%;
}

/* Trace tags (Analyze -> Code -> Understand ...) */
.deepanalyze-chat-trace {
  display: inline-flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
  padding: 8px 10px;
  border: 1px solid var(--deepanalyze-border);
  border-radius: var(--deepanalyze-radius);
  background: var(--deepanalyze-bg-secondary);
  max-width: 100%;
}

.deepanalyze-chat-trace-tag {
  border: 1px solid var(--deepanalyze-border);
  background: transparent;
  color: var(--deepanalyze-text);
  border-radius: 999px;
  padding: 4px 10px;
  font-size: 0.85em;
  cursor: pointer;
}

.deepanalyze-chat-trace-tag:hover {
  background: var(--deepanalyze-bg);
}

.deepanalyze-chat-trace-tag-active {
  border-color: var(--deepanalyze-primary);
  background: var(--deepanalyze-primary);
  color: var(--deepanalyze-primary-text);
}

.deepanalyze-chat-trace-sep {
  color: var(--deepanalyze-text-secondary);
  user-select: none;
}

/* Working indicator */
.deepanalyze-chat-message-working .deepanalyze-chat-working-indicator {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 4px 0;
  color: var(--deepanalyze-text-secondary);
  font-size: 0.9em;
  letter-spacing: 0.02em;
}

.deepanalyze-chat-working-details {
  width: 100%;
}

.deepanalyze-chat-working-summary {
  list-style: none;
  cursor: pointer;
}

.deepanalyze-chat-working-summary::-webkit-details-marker {
  display: none;
}

.deepanalyze-chat-working-output {
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px solid var(--deepanalyze-border);
}

.deepanalyze-chat-working-entry + .deepanalyze-chat-working-entry {
  margin-top: 12px;
}

.deepanalyze-chat-message-working .deepanalyze-chat-working-dot {
  width: 8px;
  height: 8px;
  border-radius: 999px;
  background: var(--deepanalyze-text-secondary);
  opacity: 0.35;
  animation: deepanalyze-working-blink 1s ease-in-out infinite;
}

/* 更高优先级：避免被上面的默认 working dot 样式覆盖 */
.deepanalyze-chat-message-working.deepanalyze-chat-message-working-done
  .deepanalyze-chat-working-dot {
  animation: none;
  opacity: 1;
  background: var(--jp-success-color1, #2ea043);
}

.deepanalyze-chat-message-working.deepanalyze-chat-message-working-done
  .deepanalyze-chat-working-text {
  color: var(--deepanalyze-text-secondary);
}

.deepanalyze-chat-message-working.deepanalyze-chat-message-working-waiting
  .deepanalyze-chat-working-dot {
  animation: none;
  opacity: 1;
  background: var(--jp-warn-color1, #d29922);
}

.deepanalyze-chat-message-working.deepanalyze-chat-message-working-waiting
  .deepanalyze-chat-working-text {
  color: var(--deepanalyze-text-secondary);
}

/* scratch.ipynb：右键“使用大模型编辑”底部通知条（停止/接受/回退） */
.deepanalyze-cell-rewrite-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 8px 12px;
  background: var(--jp-layout-color0);
}

/* 重要：避免 \`.deepanalyze-cell-rewrite-bar { display:flex }\` 覆盖 HTML \`hidden\` 的默认样式 */
.deepanalyze-cell-rewrite-bar[hidden] {
  display: none !important;
}

.deepanalyze-cell-rewrite-topbar {
  margin-top: 4px;
  margin-bottom: 6px;
  border-bottom: 1px solid var(--jp-border-color2);
}

.deepanalyze-cell-rewrite-bottombar {
  margin-top: 6px;
  border-top: 1px solid var(--jp-border-color2);
}

.deepanalyze-cell-rewrite-status {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  min-height: 22px;
  color: var(--deepanalyze-text-secondary);
  font-size: var(--jp-ui-font-size1);
}

.deepanalyze-cell-rewrite-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--jp-border-color2);
  display: inline-block;
  opacity: 0.55;
}

.deepanalyze-cell-rewrite-dot-working {
  animation: deepanalyze-working-blink 1.2s infinite;
  opacity: 1;
}

.deepanalyze-cell-rewrite-actions {
  display: inline-flex;
  align-items: center;
  gap: 10px;
}

.deepanalyze-cell-rewrite-stop,
.deepanalyze-cell-rewrite-accept,
.deepanalyze-cell-rewrite-rollback {
  border: 1px solid var(--jp-border-color2);
  background: var(--jp-layout-color1);
  color: var(--jp-ui-font-color1);
  border-radius: 6px;
  padding: 4px 12px;
  font-size: var(--jp-ui-font-size1);
  line-height: 1.4;
  cursor: pointer;
}

.deepanalyze-cell-rewrite-stop:hover,
.deepanalyze-cell-rewrite-accept:hover,
.deepanalyze-cell-rewrite-rollback:hover {
  background: var(--jp-layout-color2);
}

/* 生成结束：接受/回退按钮强调色 */
.deepanalyze-cell-rewrite-accept {
  border-color: var(--jp-success-color1, #2ea043);
  background: color-mix(in srgb, var(--jp-success-color1, #2ea043) 12%, var(--jp-layout-color1));
  color: var(--jp-ui-font-color1);
}

.deepanalyze-cell-rewrite-accept:hover {
  background: color-mix(in srgb, var(--jp-success-color1, #2ea043) 18%, var(--jp-layout-color1));
}

.deepanalyze-cell-rewrite-rollback {
  border-color: var(--jp-error-color1, #cf222e);
  background: color-mix(in srgb, var(--jp-error-color1, #cf222e) 12%, var(--jp-layout-color1));
  color: var(--jp-ui-font-color1);
}

.deepanalyze-cell-rewrite-rollback:hover {
  background: color-mix(in srgb, var(--jp-error-color1, #cf222e) 18%, var(--jp-layout-color1));
}

@keyframes deepanalyze-working-blink {
  0%,
  100% {
    opacity: 0.25;
  }
  50% {
    opacity: 0.95;
  }
}

/* System Message Style */
.deepanalyze-chat-message-system .deepanalyze-chat-bubble {
  background: var(--jp-layout-color3);
  border-left: 4px solid var(--jp-error-color1);
  color: var(--deepanalyze-text);
  font-size: 0.9em;
  padding: 8px 12px;
}

/* Modules (Analyze, Code, etc.) */
.deepanalyze-chat-module {
  border: none;
  background: transparent;
  margin-top: 8px;
}

.deepanalyze-chat-module-summary {
  cursor: pointer;
  user-select: none;
  padding: 4px 0;
  background: transparent;
  font-weight: 600;
  font-size: 0.85em;
  color: var(--deepanalyze-text);
  display: flex;
  align-items: center;
  border-bottom: 1px solid var(--deepanalyze-border);
}

.deepanalyze-chat-module-summary::before {
  content: '▶';
  display: inline-block;
  margin-right: 8px;
  font-size: 0.8em;
  transition: transform 0.2s;
}

.deepanalyze-chat-module[open] .deepanalyze-chat-module-summary::before {
  transform: rotate(90deg);
}

.deepanalyze-chat-module[open] .deepanalyze-chat-module-summary {
  border-bottom-color: var(--deepanalyze-primary);
}

.deepanalyze-chat-module-content {
  padding: 8px 0;
  font-size: 0.95em;
  background: transparent;
}

/* 生成过程（下拉栏 A）与块级输出（下拉栏 X） */
.deepanalyze-chat-stream {
  margin-top: 3px;
}

.deepanalyze-chat-stream-root {
  border: none;
  background: transparent;
}

.deepanalyze-chat-stream-root-summary {
  list-style: none;
  cursor: pointer;
  user-select: none;
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 1px 0;
  font-size: 0.82em;
  color: var(--deepanalyze-text-secondary);
}

.deepanalyze-chat-stream-root-summary::-webkit-details-marker {
  display: none;
}

.deepanalyze-chat-stream-root-summary::marker {
  content: '';
}

.deepanalyze-chat-stream-block {
  border: none;
  background: transparent;
  margin-top: 1px;
}

.deepanalyze-chat-stream-block-summary {
  list-style: none;
  cursor: pointer;
  user-select: none;
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 1px 0;
  font-size: 0.82em;
  color: var(--deepanalyze-text);
}

.deepanalyze-chat-stream-block-summary::-webkit-details-marker {
  display: none;
}

.deepanalyze-chat-stream-block-summary::marker {
  content: '';
}

.deepanalyze-chat-stream-block-content {
  margin: 1px 0 0 0;
  padding: 0;
  font-size: 0.78em;
  line-height: 1.35;
}

.deepanalyze-chat-stream-answer-panel {
  border: none;
  background: transparent;
  margin-top: 2px;
}

.deepanalyze-chat-stream-answer-summary {
  list-style: none;
  cursor: pointer;
  user-select: none;
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 1px 0;
  font-size: 0.82em;
  color: var(--deepanalyze-text);
}

.deepanalyze-chat-stream-answer-summary::-webkit-details-marker {
  display: none;
}

.deepanalyze-chat-stream-answer-summary::marker {
  content: '';
}

.deepanalyze-chat-stream-answer-content {
  margin-top: 2px;
  font-size: 0.82em;
  line-height: 1.35;
  color: var(--deepanalyze-text);
}

.deepanalyze-chat-stream-answer-content > :first-child {
  margin-top: 0;
}

.deepanalyze-chat-stream-answer-content > :last-child {
  margin-bottom: 0;
}

.deepanalyze-chat-stream-inner {
  margin-top: 1px;
  margin-left: 10px;
  padding-left: 10px;
  border-left: 1px solid var(--deepanalyze-border);
}

.deepanalyze-chat-stream-block-content-markdown {
  white-space: normal;
  word-break: break-word;
  color: var(--deepanalyze-text-secondary);
  max-height: 220px;
  overflow: auto;
}

.deepanalyze-chat-stream-block-content-markdown > :first-child {
  margin-top: 0;
}

.deepanalyze-chat-stream-block-content-markdown > :last-child {
  margin-bottom: 0;
}

.deepanalyze-chat-stream-block-content-code {
  padding: 6px 8px;
  background: var(--deepanalyze-bg-secondary);
  border: 1px solid var(--deepanalyze-border);
  border-radius: 4px;
  overflow-x: auto;
  overflow-y: auto;
  max-height: 220px;
}

.deepanalyze-chat-stream-code {
  display: block;
  white-space: pre;
  word-break: normal;
  font-family: var(--jp-code-font-family);
  font-size: 0.78em;
  line-height: 1.35;
  color: var(--deepanalyze-text);
}

.deepanalyze-code-keyword {
  color: var(--jp-mirror-editor-keyword-color, var(--jp-brand-color1));
  font-weight: 600;
}

.deepanalyze-code-string {
  color: var(--jp-mirror-editor-string-color, #a6d6ff);
}

.deepanalyze-code-comment {
  color: var(--jp-mirror-editor-comment-color, var(--deepanalyze-text-secondary));
  font-style: italic;
}

.deepanalyze-chat-stream-spinner {
  width: 14px;
  height: 14px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex: 0 0 auto;
  color: var(--deepanalyze-text-secondary);
}

.deepanalyze-chat-stream-spinner[hidden] {
  display: none !important;
}

.deepanalyze-chat-stream-spinner::before {
  content: '↻';
  display: inline-block;
  animation: deepanalyze-chat-spin 1s linear infinite;
  transform-origin: 50% 50%;
}

.deepanalyze-chat-stream-caret {
  width: 14px;
  height: 14px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex: 0 0 auto;
  color: var(--deepanalyze-text-secondary);
}

.deepanalyze-chat-stream-caret[hidden] {
  display: none !important;
}

.deepanalyze-chat-stream-caret::before {
  content: '';
  display: inline-block;
  width: 6px;
  height: 6px;
  border-right: 2px solid currentColor;
  border-bottom: 2px solid currentColor;
  transform: rotate(-45deg);
  transition: transform 0.15s ease;
  transform-origin: 50% 50%;
}

.deepanalyze-chat-stream-root[open]
  > .deepanalyze-chat-stream-root-summary
  .deepanalyze-chat-stream-caret::before {
  transform: rotate(45deg);
}

.deepanalyze-chat-stream-block[open]
  > .deepanalyze-chat-stream-block-summary
  .deepanalyze-chat-stream-caret::before {
  transform: rotate(45deg);
}

.deepanalyze-chat-stream-answer-panel[open]
  > .deepanalyze-chat-stream-answer-summary
  .deepanalyze-chat-stream-caret::before {
  transform: rotate(45deg);
}

@keyframes deepanalyze-chat-spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* Input Area */
.deepanalyze-chat-input-wrapper {
  flex: 0 0 auto;
  padding: 8px 10px;
  background: var(--deepanalyze-bg);
  border-top: 1px solid var(--deepanalyze-border);
}

.deepanalyze-chat-composer {
  display: flex;
  flex-direction: column;
  gap: 6px;
  border: 1px solid var(--deepanalyze-border);
  border-radius: var(--deepanalyze-radius);
  padding: 8px 10px;
  background: var(--deepanalyze-input-bg);
  transition: border-color 0.2s, box-shadow 0.2s;
}

.deepanalyze-chat-composer:focus-within {
  border-color: var(--deepanalyze-primary);
  box-shadow: 0 0 0 2px rgba(var(--deepanalyze-primary), 0.2); /* Note: rgba might not work with var, relying on fallback or simple focus */
}

.deepanalyze-chat-input {
  width: 100%;
  resize: none;
  min-height: 20px;
  max-height: 120px;
  border: none;
  background: transparent;
  color: var(--deepanalyze-text);
  outline: none;
  font-family: inherit;
  font-size: inherit;
  line-height: 1.5;
}

.deepanalyze-chat-actions {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 8px;
}

.deepanalyze-chat-model-selector {
  margin-right: auto;
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.deepanalyze-chat-model-button {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  border: 1px solid var(--deepanalyze-border);
  border-radius: 6px;
  padding: 6px 10px;
  background: var(--deepanalyze-input-bg);
  color: var(--deepanalyze-text);
  cursor: pointer;
  font-size: 0.85em;
}

.deepanalyze-chat-model-button:hover {
  border-color: var(--deepanalyze-primary);
}

.deepanalyze-chat-lang-select {
  height: 28px;
  border: 1px solid var(--deepanalyze-border);
  border-radius: 6px;
  padding: 4px 8px;
  background: var(--deepanalyze-input-bg);
  color: var(--deepanalyze-text);
  cursor: pointer;
  font-size: 0.85em;
}

.deepanalyze-chat-lang-select:hover {
  border-color: var(--deepanalyze-primary);
}

.deepanalyze-chat-model-add-button {
  width: 28px;
  height: 28px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: 1px solid var(--deepanalyze-border);
  border-radius: 6px;
  background: var(--deepanalyze-input-bg);
  color: var(--deepanalyze-text);
  cursor: pointer;
  font-size: 0.95em;
  line-height: 1;
}

.deepanalyze-chat-model-add-button:hover {
  border-color: var(--deepanalyze-primary);
}

.deepanalyze-chat-model-caret {
  opacity: 0.8;
}

.deepanalyze-chat-model-menu {
  position: absolute;
  left: 0;
  bottom: calc(100% + 8px);
  min-width: 200px;
  max-width: 320px;
  max-height: 240px;
  overflow: auto;
  background: var(--deepanalyze-input-bg);
  border: 1px solid var(--deepanalyze-border);
  border-radius: 8px;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.18);
  padding: 4px;
  z-index: 9999;
}

.deepanalyze-chat-model-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 10px;
  border-radius: 6px;
  cursor: pointer;
}

.deepanalyze-chat-model-item:hover {
  background: var(--jp-layout-color2);
}

.deepanalyze-chat-model-item.is-active {
  outline: 1px solid var(--deepanalyze-primary);
}

.deepanalyze-chat-model-item-label {
  flex: 1 1 auto;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.deepanalyze-chat-model-gear {
  border: 1px solid var(--deepanalyze-border);
  border-radius: 6px;
  background: transparent;
  color: var(--deepanalyze-text-secondary);
  width: 28px;
  height: 28px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.deepanalyze-chat-model-gear:hover {
  border-color: var(--deepanalyze-primary);
  color: var(--deepanalyze-text);
}

.deepanalyze-chat-model-item-add {
  margin-top: 4px;
  border-top: 1px solid var(--deepanalyze-border);
  border-radius: 0;
  padding-top: 10px;
  color: var(--deepanalyze-text-secondary);
}

.deepanalyze-chat-model-item-add:hover {
  color: var(--deepanalyze-text);
}

.deepanalyze-chat-model-config-row {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin: 8px 0;
}

.deepanalyze-chat-model-config-label {
  font-size: 0.85em;
  color: var(--deepanalyze-text-secondary);
}

.deepanalyze-model-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  display: inline-block;
  flex: 0 0 auto;
}

.deepanalyze-model-dot-ok {
  background: var(--jp-success-color1, #2ea043);
}

.deepanalyze-model-dot-bad {
  background: var(--jp-error-color1, #d1242f);
}

.deepanalyze-chat-model-key-hint {
  margin-bottom: 8px;
  color: var(--deepanalyze-text-secondary);
}

.deepanalyze-chat-model-key-input {
  width: 100%;
  box-sizing: border-box;
  padding: 8px 10px;
  border: 1px solid var(--deepanalyze-border);
  border-radius: 6px;
  background: var(--deepanalyze-input-bg);
  color: var(--deepanalyze-text);
}

.deepanalyze-chat-control-button {
  border: none;
  border-radius: 4px;
  padding: 8px 12px;
  font-weight: 500;
  font-size: 0.9em;
  cursor: pointer;
  transition: opacity 0.2s;
}

.deepanalyze-chat-control-button:disabled {
  background: var(--jp-layout-color3);
  color: var(--deepanalyze-text-secondary);
  opacity: 0.8;
  cursor: not-allowed;
}

.deepanalyze-chat-continue-button {
  background: var(--jp-success-color1, #2ea043);
  color: #ffffff;
}

.deepanalyze-chat-abort-button {
  background: var(--jp-error-color1);
  color: #ffffff;
}

.deepanalyze-chat-auto-toggle {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 0 6px;
  color: var(--deepanalyze-text-secondary);
  user-select: none;
  font-size: 0.9em;
}

.deepanalyze-chat-auto-toggle input[type='checkbox'] {
  transform: translateY(0.5px);
}

.deepanalyze-chat-send-button {
  border: none;
  border-radius: 4px;
  padding: 6px 12px;
  background: var(--deepanalyze-primary);
  color: var(--deepanalyze-primary-text);
  font-weight: 500;
  font-size: 0.9em;
  cursor: pointer;
  transition: opacity 0.2s;
}

.deepanalyze-chat-send-button:hover {
  opacity: 0.9;
}

.deepanalyze-chat-send-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Scrollbar */
.deepanalyze-chat-messages::-webkit-scrollbar {
  width: 8px;
}

.deepanalyze-chat-messages::-webkit-scrollbar-track {
  background: transparent;
}

.deepanalyze-chat-messages::-webkit-scrollbar-thumb {
  background: var(--jp-layout-color3);
  border-radius: 4px;
}

.deepanalyze-chat-messages::-webkit-scrollbar-thumb:hover {
  background: var(--jp-layout-color4);
}

.deepanalyze-hidden-tabbar {
  display: none !important;
}

.deepanalyze-launcher-icon {
  background-image: url(${___CSS_LOADER_URL_REPLACEMENT_0___});
  background-repeat: no-repeat;
  background-position: center;
  background-size: contain;
}

/* Markdown Content Styling */
.deepanalyze-chat-bubble p {
  margin-bottom: 0.8em;
}

.deepanalyze-chat-bubble p:last-child {
  margin-bottom: 0;
}

.deepanalyze-chat-bubble pre {
  background: var(--jp-layout-color2);
  padding: 12px;
  border-radius: 4px;
  overflow-x: auto;
  margin: 10px 0;
}

.deepanalyze-chat-bubble code {
  font-family: var(--jp-code-font-family);
  background: rgba(127, 127, 127, 0.15);
  padding: 2px 4px;
  border-radius: 3px;
  font-size: 0.9em;
}

.deepanalyze-chat-bubble pre code {
  background: transparent;
  padding: 0;
  color: inherit;
}

.deepanalyze-chat-bubble a {
  color: var(--deepanalyze-primary);
  text-decoration: none;
}

.deepanalyze-chat-bubble a:hover {
  text-decoration: underline;
}
`, "",{"version":3,"sources":["webpack://./style/base.css"],"names":[],"mappings":"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","sourcesContent":["/*\n    See the JupyterLab Developer Guide for useful CSS Patterns:\n\n    https://jupyterlab.readthedocs.io/en/stable/developer/css.html\n*/\n\n.deepanalyze-chat-panel {\n  /* Modern VS Code / Cursor inspired variables */\n  --deepanalyze-bg: var(--jp-layout-color1);\n  --deepanalyze-bg-secondary: var(--jp-layout-color2);\n  --deepanalyze-border: var(--jp-border-color2);\n  --deepanalyze-text: var(--jp-ui-font-color1);\n  --deepanalyze-text-secondary: var(--jp-ui-font-color2);\n  --deepanalyze-primary: var(--jp-brand-color1);\n  --deepanalyze-primary-hover: var(--jp-brand-color0);\n  --deepanalyze-primary-text: #ffffff;\n  --deepanalyze-radius: 6px;\n  --deepanalyze-input-bg: var(--jp-layout-color0);\n  --deepanalyze-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);\n\n  display: flex;\n  flex-direction: column;\n  height: 100%;\n  min-height: 0;\n  background: var(--deepanalyze-bg);\n  color: var(--deepanalyze-text);\n  font-family: var(--jp-ui-font-family);\n  font-size: var(--jp-ui-font-size1);\n  padding: 0; /* Remove padding to fill the tab */\n}\n\n.deepanalyze-chat-card {\n  flex: 1 1 auto;\n  min-height: 0;\n  display: flex;\n  flex-direction: column;\n  border: none; /* Remove border */\n  border-radius: 0; /* Remove radius */\n  background: var(--deepanalyze-bg);\n  overflow: hidden;\n}\n\n/* Header */\n.deepanalyze-chat-panel-header {\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  padding: 8px 16px;\n  border-bottom: 1px solid var(--deepanalyze-border);\n  background: var(--deepanalyze-bg);\n  font-size: 0.9em;\n  font-weight: 600;\n  color: var(--deepanalyze-text-secondary);\n  text-transform: uppercase;\n  letter-spacing: 0.05em;\n}\n\n.deepanalyze-chat-panel-title {\n  overflow: hidden;\n  text-overflow: ellipsis;\n  white-space: nowrap;\n}\n\n.deepanalyze-chat-panel-actions {\n  display: flex;\n  align-items: center;\n  gap: 8px;\n}\n\n.deepanalyze-chat-exit-button {\n  border: none;\n  border-radius: 4px;\n  padding: 8px 16px;\n  background: transparent;\n  color: var(--deepanalyze-text-secondary);\n  cursor: pointer;\n  font-size: 1em;\n  font-weight: 600;\n  transition: background 0.2s, color 0.2s;\n}\n\n.deepanalyze-chat-exit-button:hover {\n  background: var(--deepanalyze-bg-secondary);\n  color: var(--deepanalyze-text);\n}\n\n/* Messages Area */\n.deepanalyze-chat-messages {\n  flex: 1 1 auto;\n  min-height: 0;\n  overflow-y: auto;\n  padding: 20px;\n  display: flex;\n  flex-direction: column;\n  gap: 24px; /* More space between messages */\n  background: var(--deepanalyze-bg);\n}\n\n.deepanalyze-chat-message {\n  display: flex;\n  flex-direction: column;\n  gap: 6px;\n  max-width: 100%;\n}\n\n.deepanalyze-chat-message-user {\n  align-items: flex-end;\n}\n\n.deepanalyze-chat-message-assistant,\n.deepanalyze-chat-message-system {\n  align-items: flex-start;\n}\n\n.deepanalyze-chat-bubble {\n  max-width: 90%;\n  padding: 10px 14px;\n  border-radius: var(--deepanalyze-radius);\n  line-height: 1.6;\n  font-size: var(--jp-ui-font-size1);\n  position: relative;\n}\n\n/* User Message Style */\n.deepanalyze-chat-message-user .deepanalyze-chat-bubble {\n  background: var(--deepanalyze-primary);\n  color: var(--deepanalyze-primary-text);\n  border-bottom-right-radius: 2px;\n  box-shadow: var(--deepanalyze-shadow);\n}\n\n/* Assistant Message Style */\n.deepanalyze-chat-message-assistant .deepanalyze-chat-bubble {\n  background: transparent;\n  color: var(--deepanalyze-text);\n  padding: 0; /* Remove padding for assistant to align with code blocks */\n  max-width: 100%;\n  width: 100%;\n}\n\n/* Trace tags (Analyze -> Code -> Understand ...) */\n.deepanalyze-chat-trace {\n  display: inline-flex;\n  align-items: center;\n  flex-wrap: wrap;\n  gap: 8px;\n  padding: 8px 10px;\n  border: 1px solid var(--deepanalyze-border);\n  border-radius: var(--deepanalyze-radius);\n  background: var(--deepanalyze-bg-secondary);\n  max-width: 100%;\n}\n\n.deepanalyze-chat-trace-tag {\n  border: 1px solid var(--deepanalyze-border);\n  background: transparent;\n  color: var(--deepanalyze-text);\n  border-radius: 999px;\n  padding: 4px 10px;\n  font-size: 0.85em;\n  cursor: pointer;\n}\n\n.deepanalyze-chat-trace-tag:hover {\n  background: var(--deepanalyze-bg);\n}\n\n.deepanalyze-chat-trace-tag-active {\n  border-color: var(--deepanalyze-primary);\n  background: var(--deepanalyze-primary);\n  color: var(--deepanalyze-primary-text);\n}\n\n.deepanalyze-chat-trace-sep {\n  color: var(--deepanalyze-text-secondary);\n  user-select: none;\n}\n\n/* Working indicator */\n.deepanalyze-chat-message-working .deepanalyze-chat-working-indicator {\n  display: inline-flex;\n  align-items: center;\n  gap: 8px;\n  padding: 4px 0;\n  color: var(--deepanalyze-text-secondary);\n  font-size: 0.9em;\n  letter-spacing: 0.02em;\n}\n\n.deepanalyze-chat-working-details {\n  width: 100%;\n}\n\n.deepanalyze-chat-working-summary {\n  list-style: none;\n  cursor: pointer;\n}\n\n.deepanalyze-chat-working-summary::-webkit-details-marker {\n  display: none;\n}\n\n.deepanalyze-chat-working-output {\n  margin-top: 10px;\n  padding-top: 10px;\n  border-top: 1px solid var(--deepanalyze-border);\n}\n\n.deepanalyze-chat-working-entry + .deepanalyze-chat-working-entry {\n  margin-top: 12px;\n}\n\n.deepanalyze-chat-message-working .deepanalyze-chat-working-dot {\n  width: 8px;\n  height: 8px;\n  border-radius: 999px;\n  background: var(--deepanalyze-text-secondary);\n  opacity: 0.35;\n  animation: deepanalyze-working-blink 1s ease-in-out infinite;\n}\n\n/* 更高优先级：避免被上面的默认 working dot 样式覆盖 */\n.deepanalyze-chat-message-working.deepanalyze-chat-message-working-done\n  .deepanalyze-chat-working-dot {\n  animation: none;\n  opacity: 1;\n  background: var(--jp-success-color1, #2ea043);\n}\n\n.deepanalyze-chat-message-working.deepanalyze-chat-message-working-done\n  .deepanalyze-chat-working-text {\n  color: var(--deepanalyze-text-secondary);\n}\n\n.deepanalyze-chat-message-working.deepanalyze-chat-message-working-waiting\n  .deepanalyze-chat-working-dot {\n  animation: none;\n  opacity: 1;\n  background: var(--jp-warn-color1, #d29922);\n}\n\n.deepanalyze-chat-message-working.deepanalyze-chat-message-working-waiting\n  .deepanalyze-chat-working-text {\n  color: var(--deepanalyze-text-secondary);\n}\n\n/* scratch.ipynb：右键“使用大模型编辑”底部通知条（停止/接受/回退） */\n.deepanalyze-cell-rewrite-bar {\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  gap: 12px;\n  padding: 8px 12px;\n  background: var(--jp-layout-color0);\n}\n\n/* 重要：避免 `.deepanalyze-cell-rewrite-bar { display:flex }` 覆盖 HTML `hidden` 的默认样式 */\n.deepanalyze-cell-rewrite-bar[hidden] {\n  display: none !important;\n}\n\n.deepanalyze-cell-rewrite-topbar {\n  margin-top: 4px;\n  margin-bottom: 6px;\n  border-bottom: 1px solid var(--jp-border-color2);\n}\n\n.deepanalyze-cell-rewrite-bottombar {\n  margin-top: 6px;\n  border-top: 1px solid var(--jp-border-color2);\n}\n\n.deepanalyze-cell-rewrite-status {\n  display: inline-flex;\n  align-items: center;\n  gap: 8px;\n  min-height: 22px;\n  color: var(--deepanalyze-text-secondary);\n  font-size: var(--jp-ui-font-size1);\n}\n\n.deepanalyze-cell-rewrite-dot {\n  width: 10px;\n  height: 10px;\n  border-radius: 50%;\n  background: var(--jp-border-color2);\n  display: inline-block;\n  opacity: 0.55;\n}\n\n.deepanalyze-cell-rewrite-dot-working {\n  animation: deepanalyze-working-blink 1.2s infinite;\n  opacity: 1;\n}\n\n.deepanalyze-cell-rewrite-actions {\n  display: inline-flex;\n  align-items: center;\n  gap: 10px;\n}\n\n.deepanalyze-cell-rewrite-stop,\n.deepanalyze-cell-rewrite-accept,\n.deepanalyze-cell-rewrite-rollback {\n  border: 1px solid var(--jp-border-color2);\n  background: var(--jp-layout-color1);\n  color: var(--jp-ui-font-color1);\n  border-radius: 6px;\n  padding: 4px 12px;\n  font-size: var(--jp-ui-font-size1);\n  line-height: 1.4;\n  cursor: pointer;\n}\n\n.deepanalyze-cell-rewrite-stop:hover,\n.deepanalyze-cell-rewrite-accept:hover,\n.deepanalyze-cell-rewrite-rollback:hover {\n  background: var(--jp-layout-color2);\n}\n\n/* 生成结束：接受/回退按钮强调色 */\n.deepanalyze-cell-rewrite-accept {\n  border-color: var(--jp-success-color1, #2ea043);\n  background: color-mix(in srgb, var(--jp-success-color1, #2ea043) 12%, var(--jp-layout-color1));\n  color: var(--jp-ui-font-color1);\n}\n\n.deepanalyze-cell-rewrite-accept:hover {\n  background: color-mix(in srgb, var(--jp-success-color1, #2ea043) 18%, var(--jp-layout-color1));\n}\n\n.deepanalyze-cell-rewrite-rollback {\n  border-color: var(--jp-error-color1, #cf222e);\n  background: color-mix(in srgb, var(--jp-error-color1, #cf222e) 12%, var(--jp-layout-color1));\n  color: var(--jp-ui-font-color1);\n}\n\n.deepanalyze-cell-rewrite-rollback:hover {\n  background: color-mix(in srgb, var(--jp-error-color1, #cf222e) 18%, var(--jp-layout-color1));\n}\n\n@keyframes deepanalyze-working-blink {\n  0%,\n  100% {\n    opacity: 0.25;\n  }\n  50% {\n    opacity: 0.95;\n  }\n}\n\n/* System Message Style */\n.deepanalyze-chat-message-system .deepanalyze-chat-bubble {\n  background: var(--jp-layout-color3);\n  border-left: 4px solid var(--jp-error-color1);\n  color: var(--deepanalyze-text);\n  font-size: 0.9em;\n  padding: 8px 12px;\n}\n\n/* Modules (Analyze, Code, etc.) */\n.deepanalyze-chat-module {\n  border: none;\n  background: transparent;\n  margin-top: 8px;\n}\n\n.deepanalyze-chat-module-summary {\n  cursor: pointer;\n  user-select: none;\n  padding: 4px 0;\n  background: transparent;\n  font-weight: 600;\n  font-size: 0.85em;\n  color: var(--deepanalyze-text);\n  display: flex;\n  align-items: center;\n  border-bottom: 1px solid var(--deepanalyze-border);\n}\n\n.deepanalyze-chat-module-summary::before {\n  content: '▶';\n  display: inline-block;\n  margin-right: 8px;\n  font-size: 0.8em;\n  transition: transform 0.2s;\n}\n\n.deepanalyze-chat-module[open] .deepanalyze-chat-module-summary::before {\n  transform: rotate(90deg);\n}\n\n.deepanalyze-chat-module[open] .deepanalyze-chat-module-summary {\n  border-bottom-color: var(--deepanalyze-primary);\n}\n\n.deepanalyze-chat-module-content {\n  padding: 8px 0;\n  font-size: 0.95em;\n  background: transparent;\n}\n\n/* 生成过程（下拉栏 A）与块级输出（下拉栏 X） */\n.deepanalyze-chat-stream {\n  margin-top: 3px;\n}\n\n.deepanalyze-chat-stream-root {\n  border: none;\n  background: transparent;\n}\n\n.deepanalyze-chat-stream-root-summary {\n  list-style: none;\n  cursor: pointer;\n  user-select: none;\n  display: flex;\n  align-items: center;\n  gap: 4px;\n  padding: 1px 0;\n  font-size: 0.82em;\n  color: var(--deepanalyze-text-secondary);\n}\n\n.deepanalyze-chat-stream-root-summary::-webkit-details-marker {\n  display: none;\n}\n\n.deepanalyze-chat-stream-root-summary::marker {\n  content: '';\n}\n\n.deepanalyze-chat-stream-block {\n  border: none;\n  background: transparent;\n  margin-top: 1px;\n}\n\n.deepanalyze-chat-stream-block-summary {\n  list-style: none;\n  cursor: pointer;\n  user-select: none;\n  display: flex;\n  align-items: center;\n  gap: 4px;\n  padding: 1px 0;\n  font-size: 0.82em;\n  color: var(--deepanalyze-text);\n}\n\n.deepanalyze-chat-stream-block-summary::-webkit-details-marker {\n  display: none;\n}\n\n.deepanalyze-chat-stream-block-summary::marker {\n  content: '';\n}\n\n.deepanalyze-chat-stream-block-content {\n  margin: 1px 0 0 0;\n  padding: 0;\n  font-size: 0.78em;\n  line-height: 1.35;\n}\n\n.deepanalyze-chat-stream-answer-panel {\n  border: none;\n  background: transparent;\n  margin-top: 2px;\n}\n\n.deepanalyze-chat-stream-answer-summary {\n  list-style: none;\n  cursor: pointer;\n  user-select: none;\n  display: flex;\n  align-items: center;\n  gap: 4px;\n  padding: 1px 0;\n  font-size: 0.82em;\n  color: var(--deepanalyze-text);\n}\n\n.deepanalyze-chat-stream-answer-summary::-webkit-details-marker {\n  display: none;\n}\n\n.deepanalyze-chat-stream-answer-summary::marker {\n  content: '';\n}\n\n.deepanalyze-chat-stream-answer-content {\n  margin-top: 2px;\n  font-size: 0.82em;\n  line-height: 1.35;\n  color: var(--deepanalyze-text);\n}\n\n.deepanalyze-chat-stream-answer-content > :first-child {\n  margin-top: 0;\n}\n\n.deepanalyze-chat-stream-answer-content > :last-child {\n  margin-bottom: 0;\n}\n\n.deepanalyze-chat-stream-inner {\n  margin-top: 1px;\n  margin-left: 10px;\n  padding-left: 10px;\n  border-left: 1px solid var(--deepanalyze-border);\n}\n\n.deepanalyze-chat-stream-block-content-markdown {\n  white-space: normal;\n  word-break: break-word;\n  color: var(--deepanalyze-text-secondary);\n  max-height: 220px;\n  overflow: auto;\n}\n\n.deepanalyze-chat-stream-block-content-markdown > :first-child {\n  margin-top: 0;\n}\n\n.deepanalyze-chat-stream-block-content-markdown > :last-child {\n  margin-bottom: 0;\n}\n\n.deepanalyze-chat-stream-block-content-code {\n  padding: 6px 8px;\n  background: var(--deepanalyze-bg-secondary);\n  border: 1px solid var(--deepanalyze-border);\n  border-radius: 4px;\n  overflow-x: auto;\n  overflow-y: auto;\n  max-height: 220px;\n}\n\n.deepanalyze-chat-stream-code {\n  display: block;\n  white-space: pre;\n  word-break: normal;\n  font-family: var(--jp-code-font-family);\n  font-size: 0.78em;\n  line-height: 1.35;\n  color: var(--deepanalyze-text);\n}\n\n.deepanalyze-code-keyword {\n  color: var(--jp-mirror-editor-keyword-color, var(--jp-brand-color1));\n  font-weight: 600;\n}\n\n.deepanalyze-code-string {\n  color: var(--jp-mirror-editor-string-color, #a6d6ff);\n}\n\n.deepanalyze-code-comment {\n  color: var(--jp-mirror-editor-comment-color, var(--deepanalyze-text-secondary));\n  font-style: italic;\n}\n\n.deepanalyze-chat-stream-spinner {\n  width: 14px;\n  height: 14px;\n  display: inline-flex;\n  align-items: center;\n  justify-content: center;\n  flex: 0 0 auto;\n  color: var(--deepanalyze-text-secondary);\n}\n\n.deepanalyze-chat-stream-spinner[hidden] {\n  display: none !important;\n}\n\n.deepanalyze-chat-stream-spinner::before {\n  content: '↻';\n  display: inline-block;\n  animation: deepanalyze-chat-spin 1s linear infinite;\n  transform-origin: 50% 50%;\n}\n\n.deepanalyze-chat-stream-caret {\n  width: 14px;\n  height: 14px;\n  display: inline-flex;\n  align-items: center;\n  justify-content: center;\n  flex: 0 0 auto;\n  color: var(--deepanalyze-text-secondary);\n}\n\n.deepanalyze-chat-stream-caret[hidden] {\n  display: none !important;\n}\n\n.deepanalyze-chat-stream-caret::before {\n  content: '';\n  display: inline-block;\n  width: 6px;\n  height: 6px;\n  border-right: 2px solid currentColor;\n  border-bottom: 2px solid currentColor;\n  transform: rotate(-45deg);\n  transition: transform 0.15s ease;\n  transform-origin: 50% 50%;\n}\n\n.deepanalyze-chat-stream-root[open]\n  > .deepanalyze-chat-stream-root-summary\n  .deepanalyze-chat-stream-caret::before {\n  transform: rotate(45deg);\n}\n\n.deepanalyze-chat-stream-block[open]\n  > .deepanalyze-chat-stream-block-summary\n  .deepanalyze-chat-stream-caret::before {\n  transform: rotate(45deg);\n}\n\n.deepanalyze-chat-stream-answer-panel[open]\n  > .deepanalyze-chat-stream-answer-summary\n  .deepanalyze-chat-stream-caret::before {\n  transform: rotate(45deg);\n}\n\n@keyframes deepanalyze-chat-spin {\n  from {\n    transform: rotate(0deg);\n  }\n  to {\n    transform: rotate(360deg);\n  }\n}\n\n/* Input Area */\n.deepanalyze-chat-input-wrapper {\n  flex: 0 0 auto;\n  padding: 8px 10px;\n  background: var(--deepanalyze-bg);\n  border-top: 1px solid var(--deepanalyze-border);\n}\n\n.deepanalyze-chat-composer {\n  display: flex;\n  flex-direction: column;\n  gap: 6px;\n  border: 1px solid var(--deepanalyze-border);\n  border-radius: var(--deepanalyze-radius);\n  padding: 8px 10px;\n  background: var(--deepanalyze-input-bg);\n  transition: border-color 0.2s, box-shadow 0.2s;\n}\n\n.deepanalyze-chat-composer:focus-within {\n  border-color: var(--deepanalyze-primary);\n  box-shadow: 0 0 0 2px rgba(var(--deepanalyze-primary), 0.2); /* Note: rgba might not work with var, relying on fallback or simple focus */\n}\n\n.deepanalyze-chat-input {\n  width: 100%;\n  resize: none;\n  min-height: 20px;\n  max-height: 120px;\n  border: none;\n  background: transparent;\n  color: var(--deepanalyze-text);\n  outline: none;\n  font-family: inherit;\n  font-size: inherit;\n  line-height: 1.5;\n}\n\n.deepanalyze-chat-actions {\n  display: flex;\n  justify-content: flex-end;\n  align-items: center;\n  gap: 8px;\n}\n\n.deepanalyze-chat-model-selector {\n  margin-right: auto;\n  position: relative;\n  display: inline-flex;\n  align-items: center;\n  gap: 6px;\n}\n\n.deepanalyze-chat-model-button {\n  display: inline-flex;\n  align-items: center;\n  gap: 6px;\n  border: 1px solid var(--deepanalyze-border);\n  border-radius: 6px;\n  padding: 6px 10px;\n  background: var(--deepanalyze-input-bg);\n  color: var(--deepanalyze-text);\n  cursor: pointer;\n  font-size: 0.85em;\n}\n\n.deepanalyze-chat-model-button:hover {\n  border-color: var(--deepanalyze-primary);\n}\n\n.deepanalyze-chat-lang-select {\n  height: 28px;\n  border: 1px solid var(--deepanalyze-border);\n  border-radius: 6px;\n  padding: 4px 8px;\n  background: var(--deepanalyze-input-bg);\n  color: var(--deepanalyze-text);\n  cursor: pointer;\n  font-size: 0.85em;\n}\n\n.deepanalyze-chat-lang-select:hover {\n  border-color: var(--deepanalyze-primary);\n}\n\n.deepanalyze-chat-model-add-button {\n  width: 28px;\n  height: 28px;\n  display: inline-flex;\n  align-items: center;\n  justify-content: center;\n  border: 1px solid var(--deepanalyze-border);\n  border-radius: 6px;\n  background: var(--deepanalyze-input-bg);\n  color: var(--deepanalyze-text);\n  cursor: pointer;\n  font-size: 0.95em;\n  line-height: 1;\n}\n\n.deepanalyze-chat-model-add-button:hover {\n  border-color: var(--deepanalyze-primary);\n}\n\n.deepanalyze-chat-model-caret {\n  opacity: 0.8;\n}\n\n.deepanalyze-chat-model-menu {\n  position: absolute;\n  left: 0;\n  bottom: calc(100% + 8px);\n  min-width: 200px;\n  max-width: 320px;\n  max-height: 240px;\n  overflow: auto;\n  background: var(--deepanalyze-input-bg);\n  border: 1px solid var(--deepanalyze-border);\n  border-radius: 8px;\n  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.18);\n  padding: 4px;\n  z-index: 9999;\n}\n\n.deepanalyze-chat-model-item {\n  display: flex;\n  align-items: center;\n  gap: 8px;\n  padding: 8px 10px;\n  border-radius: 6px;\n  cursor: pointer;\n}\n\n.deepanalyze-chat-model-item:hover {\n  background: var(--jp-layout-color2);\n}\n\n.deepanalyze-chat-model-item.is-active {\n  outline: 1px solid var(--deepanalyze-primary);\n}\n\n.deepanalyze-chat-model-item-label {\n  flex: 1 1 auto;\n  white-space: nowrap;\n  overflow: hidden;\n  text-overflow: ellipsis;\n}\n\n.deepanalyze-chat-model-gear {\n  border: 1px solid var(--deepanalyze-border);\n  border-radius: 6px;\n  background: transparent;\n  color: var(--deepanalyze-text-secondary);\n  width: 28px;\n  height: 28px;\n  display: inline-flex;\n  align-items: center;\n  justify-content: center;\n  cursor: pointer;\n}\n\n.deepanalyze-chat-model-gear:hover {\n  border-color: var(--deepanalyze-primary);\n  color: var(--deepanalyze-text);\n}\n\n.deepanalyze-chat-model-item-add {\n  margin-top: 4px;\n  border-top: 1px solid var(--deepanalyze-border);\n  border-radius: 0;\n  padding-top: 10px;\n  color: var(--deepanalyze-text-secondary);\n}\n\n.deepanalyze-chat-model-item-add:hover {\n  color: var(--deepanalyze-text);\n}\n\n.deepanalyze-chat-model-config-row {\n  display: flex;\n  flex-direction: column;\n  gap: 6px;\n  margin: 8px 0;\n}\n\n.deepanalyze-chat-model-config-label {\n  font-size: 0.85em;\n  color: var(--deepanalyze-text-secondary);\n}\n\n.deepanalyze-model-dot {\n  width: 8px;\n  height: 8px;\n  border-radius: 50%;\n  display: inline-block;\n  flex: 0 0 auto;\n}\n\n.deepanalyze-model-dot-ok {\n  background: var(--jp-success-color1, #2ea043);\n}\n\n.deepanalyze-model-dot-bad {\n  background: var(--jp-error-color1, #d1242f);\n}\n\n.deepanalyze-chat-model-key-hint {\n  margin-bottom: 8px;\n  color: var(--deepanalyze-text-secondary);\n}\n\n.deepanalyze-chat-model-key-input {\n  width: 100%;\n  box-sizing: border-box;\n  padding: 8px 10px;\n  border: 1px solid var(--deepanalyze-border);\n  border-radius: 6px;\n  background: var(--deepanalyze-input-bg);\n  color: var(--deepanalyze-text);\n}\n\n.deepanalyze-chat-control-button {\n  border: none;\n  border-radius: 4px;\n  padding: 8px 12px;\n  font-weight: 500;\n  font-size: 0.9em;\n  cursor: pointer;\n  transition: opacity 0.2s;\n}\n\n.deepanalyze-chat-control-button:disabled {\n  background: var(--jp-layout-color3);\n  color: var(--deepanalyze-text-secondary);\n  opacity: 0.8;\n  cursor: not-allowed;\n}\n\n.deepanalyze-chat-continue-button {\n  background: var(--jp-success-color1, #2ea043);\n  color: #ffffff;\n}\n\n.deepanalyze-chat-abort-button {\n  background: var(--jp-error-color1);\n  color: #ffffff;\n}\n\n.deepanalyze-chat-auto-toggle {\n  display: inline-flex;\n  align-items: center;\n  gap: 6px;\n  padding: 0 6px;\n  color: var(--deepanalyze-text-secondary);\n  user-select: none;\n  font-size: 0.9em;\n}\n\n.deepanalyze-chat-auto-toggle input[type='checkbox'] {\n  transform: translateY(0.5px);\n}\n\n.deepanalyze-chat-send-button {\n  border: none;\n  border-radius: 4px;\n  padding: 6px 12px;\n  background: var(--deepanalyze-primary);\n  color: var(--deepanalyze-primary-text);\n  font-weight: 500;\n  font-size: 0.9em;\n  cursor: pointer;\n  transition: opacity 0.2s;\n}\n\n.deepanalyze-chat-send-button:hover {\n  opacity: 0.9;\n}\n\n.deepanalyze-chat-send-button:disabled {\n  opacity: 0.5;\n  cursor: not-allowed;\n}\n\n/* Scrollbar */\n.deepanalyze-chat-messages::-webkit-scrollbar {\n  width: 8px;\n}\n\n.deepanalyze-chat-messages::-webkit-scrollbar-track {\n  background: transparent;\n}\n\n.deepanalyze-chat-messages::-webkit-scrollbar-thumb {\n  background: var(--jp-layout-color3);\n  border-radius: 4px;\n}\n\n.deepanalyze-chat-messages::-webkit-scrollbar-thumb:hover {\n  background: var(--jp-layout-color4);\n}\n\n.deepanalyze-hidden-tabbar {\n  display: none !important;\n}\n\n.deepanalyze-launcher-icon {\n  background-image: url('./logo.png');\n  background-repeat: no-repeat;\n  background-position: center;\n  background-size: contain;\n}\n\n/* Markdown Content Styling */\n.deepanalyze-chat-bubble p {\n  margin-bottom: 0.8em;\n}\n\n.deepanalyze-chat-bubble p:last-child {\n  margin-bottom: 0;\n}\n\n.deepanalyze-chat-bubble pre {\n  background: var(--jp-layout-color2);\n  padding: 12px;\n  border-radius: 4px;\n  overflow-x: auto;\n  margin: 10px 0;\n}\n\n.deepanalyze-chat-bubble code {\n  font-family: var(--jp-code-font-family);\n  background: rgba(127, 127, 127, 0.15);\n  padding: 2px 4px;\n  border-radius: 3px;\n  font-size: 0.9em;\n}\n\n.deepanalyze-chat-bubble pre code {\n  background: transparent;\n  padding: 0;\n  color: inherit;\n}\n\n.deepanalyze-chat-bubble a {\n  color: var(--deepanalyze-primary);\n  text-decoration: none;\n}\n\n.deepanalyze-chat-bubble a:hover {\n  text-decoration: underline;\n}\n"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./node_modules/css-loader/dist/runtime/api.js":
/*!*****************************************************!*\
  !*** ./node_modules/css-loader/dist/runtime/api.js ***!
  \*****************************************************/
/***/ ((module) => {



/*
  MIT License http://www.opensource.org/licenses/mit-license.php
  Author Tobias Koppers @sokra
*/
module.exports = function (cssWithMappingToString) {
  var list = [];

  // return the list of modules as css string
  list.toString = function toString() {
    return this.map(function (item) {
      var content = "";
      var needLayer = typeof item[5] !== "undefined";
      if (item[4]) {
        content += "@supports (".concat(item[4], ") {");
      }
      if (item[2]) {
        content += "@media ".concat(item[2], " {");
      }
      if (needLayer) {
        content += "@layer".concat(item[5].length > 0 ? " ".concat(item[5]) : "", " {");
      }
      content += cssWithMappingToString(item);
      if (needLayer) {
        content += "}";
      }
      if (item[2]) {
        content += "}";
      }
      if (item[4]) {
        content += "}";
      }
      return content;
    }).join("");
  };

  // import a list of modules into the list
  list.i = function i(modules, media, dedupe, supports, layer) {
    if (typeof modules === "string") {
      modules = [[null, modules, undefined]];
    }
    var alreadyImportedModules = {};
    if (dedupe) {
      for (var k = 0; k < this.length; k++) {
        var id = this[k][0];
        if (id != null) {
          alreadyImportedModules[id] = true;
        }
      }
    }
    for (var _k = 0; _k < modules.length; _k++) {
      var item = [].concat(modules[_k]);
      if (dedupe && alreadyImportedModules[item[0]]) {
        continue;
      }
      if (typeof layer !== "undefined") {
        if (typeof item[5] === "undefined") {
          item[5] = layer;
        } else {
          item[1] = "@layer".concat(item[5].length > 0 ? " ".concat(item[5]) : "", " {").concat(item[1], "}");
          item[5] = layer;
        }
      }
      if (media) {
        if (!item[2]) {
          item[2] = media;
        } else {
          item[1] = "@media ".concat(item[2], " {").concat(item[1], "}");
          item[2] = media;
        }
      }
      if (supports) {
        if (!item[4]) {
          item[4] = "".concat(supports);
        } else {
          item[1] = "@supports (".concat(item[4], ") {").concat(item[1], "}");
          item[4] = supports;
        }
      }
      list.push(item);
    }
  };
  return list;
};

/***/ }),

/***/ "./node_modules/css-loader/dist/runtime/getUrl.js":
/*!********************************************************!*\
  !*** ./node_modules/css-loader/dist/runtime/getUrl.js ***!
  \********************************************************/
/***/ ((module) => {



module.exports = function (url, options) {
  if (!options) {
    options = {};
  }
  if (!url) {
    return url;
  }
  url = String(url.__esModule ? url.default : url);

  // If url is already wrapped in quotes, remove them
  if (/^['"].*['"]$/.test(url)) {
    url = url.slice(1, -1);
  }
  if (options.hash) {
    url += options.hash;
  }

  // Should url be wrapped?
  // See https://drafts.csswg.org/css-values-3/#urls
  if (/["'() \t\n]|(%20)/.test(url) || options.needQuotes) {
    return "\"".concat(url.replace(/"/g, '\\"').replace(/\n/g, "\\n"), "\"");
  }
  return url;
};

/***/ }),

/***/ "./node_modules/css-loader/dist/runtime/sourceMaps.js":
/*!************************************************************!*\
  !*** ./node_modules/css-loader/dist/runtime/sourceMaps.js ***!
  \************************************************************/
/***/ ((module) => {



module.exports = function (item) {
  var content = item[1];
  var cssMapping = item[3];
  if (!cssMapping) {
    return content;
  }
  if (typeof btoa === "function") {
    var base64 = btoa(unescape(encodeURIComponent(JSON.stringify(cssMapping))));
    var data = "sourceMappingURL=data:application/json;charset=utf-8;base64,".concat(base64);
    var sourceMapping = "/*# ".concat(data, " */");
    return [content].concat([sourceMapping]).join("\n");
  }
  return [content].join("\n");
};

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js":
/*!****************************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js ***!
  \****************************************************************************/
/***/ ((module) => {



var stylesInDOM = [];
function getIndexByIdentifier(identifier) {
  var result = -1;
  for (var i = 0; i < stylesInDOM.length; i++) {
    if (stylesInDOM[i].identifier === identifier) {
      result = i;
      break;
    }
  }
  return result;
}
function modulesToDom(list, options) {
  var idCountMap = {};
  var identifiers = [];
  for (var i = 0; i < list.length; i++) {
    var item = list[i];
    var id = options.base ? item[0] + options.base : item[0];
    var count = idCountMap[id] || 0;
    var identifier = "".concat(id, " ").concat(count);
    idCountMap[id] = count + 1;
    var indexByIdentifier = getIndexByIdentifier(identifier);
    var obj = {
      css: item[1],
      media: item[2],
      sourceMap: item[3],
      supports: item[4],
      layer: item[5]
    };
    if (indexByIdentifier !== -1) {
      stylesInDOM[indexByIdentifier].references++;
      stylesInDOM[indexByIdentifier].updater(obj);
    } else {
      var updater = addElementStyle(obj, options);
      options.byIndex = i;
      stylesInDOM.splice(i, 0, {
        identifier: identifier,
        updater: updater,
        references: 1
      });
    }
    identifiers.push(identifier);
  }
  return identifiers;
}
function addElementStyle(obj, options) {
  var api = options.domAPI(options);
  api.update(obj);
  var updater = function updater(newObj) {
    if (newObj) {
      if (newObj.css === obj.css && newObj.media === obj.media && newObj.sourceMap === obj.sourceMap && newObj.supports === obj.supports && newObj.layer === obj.layer) {
        return;
      }
      api.update(obj = newObj);
    } else {
      api.remove();
    }
  };
  return updater;
}
module.exports = function (list, options) {
  options = options || {};
  list = list || [];
  var lastIdentifiers = modulesToDom(list, options);
  return function update(newList) {
    newList = newList || [];
    for (var i = 0; i < lastIdentifiers.length; i++) {
      var identifier = lastIdentifiers[i];
      var index = getIndexByIdentifier(identifier);
      stylesInDOM[index].references--;
    }
    var newLastIdentifiers = modulesToDom(newList, options);
    for (var _i = 0; _i < lastIdentifiers.length; _i++) {
      var _identifier = lastIdentifiers[_i];
      var _index = getIndexByIdentifier(_identifier);
      if (stylesInDOM[_index].references === 0) {
        stylesInDOM[_index].updater();
        stylesInDOM.splice(_index, 1);
      }
    }
    lastIdentifiers = newLastIdentifiers;
  };
};

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/insertBySelector.js":
/*!********************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/insertBySelector.js ***!
  \********************************************************************/
/***/ ((module) => {



var memo = {};

/* istanbul ignore next  */
function getTarget(target) {
  if (typeof memo[target] === "undefined") {
    var styleTarget = document.querySelector(target);

    // Special case to return head of iframe instead of iframe itself
    if (window.HTMLIFrameElement && styleTarget instanceof window.HTMLIFrameElement) {
      try {
        // This will throw an exception if access to iframe is blocked
        // due to cross-origin restrictions
        styleTarget = styleTarget.contentDocument.head;
      } catch (e) {
        // istanbul ignore next
        styleTarget = null;
      }
    }
    memo[target] = styleTarget;
  }
  return memo[target];
}

/* istanbul ignore next  */
function insertBySelector(insert, style) {
  var target = getTarget(insert);
  if (!target) {
    throw new Error("Couldn't find a style target. This probably means that the value for the 'insert' parameter is invalid.");
  }
  target.appendChild(style);
}
module.exports = insertBySelector;

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/insertStyleElement.js":
/*!**********************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/insertStyleElement.js ***!
  \**********************************************************************/
/***/ ((module) => {



/* istanbul ignore next  */
function insertStyleElement(options) {
  var element = document.createElement("style");
  options.setAttributes(element, options.attributes);
  options.insert(element, options.options);
  return element;
}
module.exports = insertStyleElement;

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js":
/*!**********************************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js ***!
  \**********************************************************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {



/* istanbul ignore next  */
function setAttributesWithoutAttributes(styleElement) {
  var nonce =  true ? __webpack_require__.nc : 0;
  if (nonce) {
    styleElement.setAttribute("nonce", nonce);
  }
}
module.exports = setAttributesWithoutAttributes;

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/styleDomAPI.js":
/*!***************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/styleDomAPI.js ***!
  \***************************************************************/
/***/ ((module) => {



/* istanbul ignore next  */
function apply(styleElement, options, obj) {
  var css = "";
  if (obj.supports) {
    css += "@supports (".concat(obj.supports, ") {");
  }
  if (obj.media) {
    css += "@media ".concat(obj.media, " {");
  }
  var needLayer = typeof obj.layer !== "undefined";
  if (needLayer) {
    css += "@layer".concat(obj.layer.length > 0 ? " ".concat(obj.layer) : "", " {");
  }
  css += obj.css;
  if (needLayer) {
    css += "}";
  }
  if (obj.media) {
    css += "}";
  }
  if (obj.supports) {
    css += "}";
  }
  var sourceMap = obj.sourceMap;
  if (sourceMap && typeof btoa !== "undefined") {
    css += "\n/*# sourceMappingURL=data:application/json;base64,".concat(btoa(unescape(encodeURIComponent(JSON.stringify(sourceMap)))), " */");
  }

  // For old IE
  /* istanbul ignore if  */
  options.styleTagTransform(css, styleElement, options.options);
}
function removeStyleElement(styleElement) {
  // istanbul ignore if
  if (styleElement.parentNode === null) {
    return false;
  }
  styleElement.parentNode.removeChild(styleElement);
}

/* istanbul ignore next  */
function domAPI(options) {
  if (typeof document === "undefined") {
    return {
      update: function update() {},
      remove: function remove() {}
    };
  }
  var styleElement = options.insertStyleElement(options);
  return {
    update: function update(obj) {
      apply(styleElement, options, obj);
    },
    remove: function remove() {
      removeStyleElement(styleElement);
    }
  };
}
module.exports = domAPI;

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/styleTagTransform.js":
/*!*********************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/styleTagTransform.js ***!
  \*********************************************************************/
/***/ ((module) => {



/* istanbul ignore next  */
function styleTagTransform(css, styleElement) {
  if (styleElement.styleSheet) {
    styleElement.styleSheet.cssText = css;
  } else {
    while (styleElement.firstChild) {
      styleElement.removeChild(styleElement.firstChild);
    }
    styleElement.appendChild(document.createTextNode(css));
  }
}
module.exports = styleTagTransform;

/***/ }),

/***/ "./style/base.css":
/*!************************!*\
  !*** ./style/base.css ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleDomAPI.js */ "./node_modules/style-loader/dist/runtime/styleDomAPI.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertBySelector.js */ "./node_modules/style-loader/dist/runtime/insertBySelector.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js */ "./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertStyleElement.js */ "./node_modules/style-loader/dist/runtime/insertStyleElement.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleTagTransform.js */ "./node_modules/style-loader/dist/runtime/styleTagTransform.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./base.css */ "./node_modules/css-loader/dist/cjs.js!./style/base.css");

      
      
      
      
      
      
      
      
      

var options = {};

options.styleTagTransform = (_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default());
options.setAttributes = (_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default());

      options.insert = _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default().bind(null, "head");
    
options.domAPI = (_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default());
options.insertStyleElement = (_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default());

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_6__["default"], options);




       /* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_6__["default"] && _node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals ? _node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals : undefined);


/***/ }),

/***/ "./style/index.js":
/*!************************!*\
  !*** ./style/index.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _base_css__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./base.css */ "./style/base.css");



/***/ }),

/***/ "./style/logo.png":
/*!************************!*\
  !*** ./style/logo.png ***!
  \************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

module.exports = __webpack_require__.p + "7ac9d3809b43169488e0.png";

/***/ })

}]);
//# sourceMappingURL=style_index_js.72e88ce4e0d23ed148eb.js.map