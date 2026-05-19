/**
 * 방송 재생 오류 — 패널·웹 공통 복구 모달
 */
(function () {
  "use strict";

  function $(id) {
    return document.getElementById(id);
  }

  const overlay = $("recoveryModal");
  if (!overlay) return;

  const msgEl = $("recoveryModalMessage");
  const progressWrap = $("recoveryModalProgress");
  const progressFill = $("recoveryModalProgressFill");
  const progressLabel = $("recoveryModalProgressLabel");
  const actions = $("recoveryModalActions");
  const btnCancel = $("recoveryModalCancel");
  const btnRecover = $("recoveryModalRecover");

  function showError(err) {
    err = err || {};
    if (msgEl) msgEl.textContent = err.message || "재생 오류가 발생했습니다.";
    if (progressWrap) progressWrap.hidden = true;
    if (actions) actions.hidden = false;
    overlay.hidden = false;
  }

  function hide() {
    overlay.hidden = true;
  }

  function setProgress(percent, step) {
    if (actions) actions.hidden = true;
    if (progressWrap) progressWrap.hidden = false;
    if (progressFill) progressFill.style.width = Math.max(0, Math.min(100, percent)) + "%";
    if (progressLabel) progressLabel.textContent = step || "";
  }

  function requestRecovery() {
    if (window.panelSocket && window.panelSocket.connected) {
      window.panelSocket.emit("recovery_request");
      return;
    }
    fetch("/api/recovery/start", {
      method: "POST",
      credentials: "same-origin",
      headers: { "Content-Type": "application/json" },
    }).catch(function () {});
  }

  function dismiss() {
    if (window.panelSocket && window.panelSocket.connected) {
      window.panelSocket.emit("recovery_dismiss");
    } else {
      fetch("/api/recovery/dismiss", {
        method: "POST",
        credentials: "same-origin",
      }).catch(function () {});
    }
    hide();
  }

  if (btnCancel) btnCancel.addEventListener("click", dismiss);
  if (btnRecover) {
    btnRecover.addEventListener("click", function () {
      setProgress(5, "복구 요청…");
      requestRecovery();
    });
  }

  window.PlaybackRecoveryUI = {
    showError: showError,
    hide: hide,
    setProgress: setProgress,
    bindSocket: function (socket) {
      if (!socket || socket.__recoveryBound) return;
      socket.__recoveryBound = true;
      socket.on("playback_error", function (err) {
        showError(err);
      });
      socket.on("playback_error_cleared", hide);
      socket.on("recovery_progress", function (data) {
        setProgress((data && data.percent) || 0, (data && data.step) || "");
      });
      socket.on("recovery_finished", hide);
    },
  };
})();
