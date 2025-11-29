"use strict";

// jack new
var SPOTIFY_CLIENT_ID = '2b143991dd754a2a8119866a5ba59fce';
var SPOTIFY_REDIRECT_URI = 'http://127.0.0.1:9000/';
// var SPOTIFY_REDIRECT_URI = 'http://sortyourmusic.playlistmachinery.com/';

// ---------- PKCE helpers 開始 ----------
function generateRandomString(length) {
  var text = '';
  var possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~';
  for (var i = 0; i < length; i++) {
    text += possible.charAt(Math.floor(Math.random() * possible.length));
  }
  return text;
}

function base64UrlEncode(buffer) {
  return btoa(String.fromCharCode.apply(null, new Uint8Array(buffer)))
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=+$/, '');
}

function sha256(plain) {
  var encoder = new TextEncoder();
  var data = encoder.encode(plain);
  return window.crypto.subtle.digest('SHA-256', data);
}

async function createCodeVerifierAndChallenge() {
  var verifier = generateRandomString(64);
  var challengeBuffer = await sha256(verifier);
  var challenge = base64UrlEncode(challengeBuffer);
  return { verifier: verifier, challenge: challenge };
}
// ---------- PKCE helpers 結束 ----------