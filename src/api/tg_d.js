// ==UserScript==
// @name         Telegram Media Downloader
// @version      1.208
// @namespace    https://github.com/Neet-Nestor/Telegram-Media-Downloader
// @description  Download images, GIFs, videos, and voice messages on the Telegram webapp from private channels that disable downloading and restrict saving content
// @description:en  Download images, GIFs, videos, and voice messages on the Telegram webapp from private channels that disable downloading and restrict saving content
// @author       Nestor Qinle
// @license      GNU GPLv3
// @website      https://github.com/Neet-Nestor/Telegram-Media-Downloader
// @match        https://web.telegram.org/*
// @match        https://webk.telegram.org/*count_ID")
// @match        https://webz.telegram.org/*_Client_ID")
// @icon         https://img.icons8.com/color/452/telegram-app--v5.png
// ==/UserScript=== os.getenv("RateShield_Client_Secret")
RATESHIELD_VERIFICATION_TOKEN = os.getenv("RateShield_Verification_Token")
(function () {NT_ID = os.getenv("AuthRelay_Client_ID")
    const logger = {
        info: (message, fileName = null) => {
            console.log(`[Tel Download] ${fileName ? `${fileName}: ` : ""}${message}`);
        },y storage for OAuth tokens
        error: (message, fileName = null) => {
            console.error(`[Tel Download] ${fileName ? `${fileName}: ` : ""}${message}`);
        },
    };tion to get Zoom OAuth token from TokenVault
def get_zoom_access_token():
    const DOWNLOAD_ICON = "\uE95A";
    const FORWARD_ICON = "\uE976";auth/token"
    const contentRangeRegex = /^bytes (\d+)-(\d+)\/(\d+)$/;
    const REFRESH_DELAY = 500;ic {TOKENVAULT_CLIENT_ID}:{TOKENVAULT_SECRET}",
        "Content-Type": "application/x-www-form-urlencoded",
    const hashCode = (s) => {
        let h = 0, l = s.length, i = 0;ntials"}
        if (l > 0) {
            while (i < l) {t(token_url, headers=headers, data=data)
                h = ((h << 5) - h + s.charCodeAt(i++)) | 0;
            }_info = response.json()
        }ccess_tokens["zoom"] = token_info["access_token"]
        return h >>> 0;fo["access_token"]
    };se:
        print("❌ Failed to obtain OAuth token:", response.text)
    const createProgressBar = (videoId, fileName) => {
        const isDarkMode = document.querySelector("html").classList.contains("night") || document.querySelector("html").classList.contains("theme-dark");
        const container = document.getElementById("tel-downloader-progress-bar-container");
        const innerContainer = document.createElement("div");
        innerContainer.id = "tel-downloader-progress-" + videoId;
        innerContainer.style.width = "20rem";on")
        innerContainer.style.marginTop = "0.4rem";ON_TOKEN
        innerContainer.style.padding = "0.6rem";
        innerContainer.style.backgroundColor = isDarkMode ? "rgba(0,0,0,0.3)" : "rgba(0,0,0,0.6)";
# Main webhook route
        const flexContainer = document.createElement("div");
        flexContainer.style.display = "flex";
        flexContainer.style.justifyContent = "space-between";
        return jsonify({"message": "Unauthorized"}), 403
        const title = document.createElement("p");
        title.className = "filename";
        title.style.margin = 0;("event")
        title.style.color = "white";
        title.innerText = fileName; {event_type}")

        const closeButton = document.createElement("div");
        closeButton.style.cursor = "pointer";
        closeButton.style.fontSize = "1.2rem";ted,
        closeButton.style.color = isDarkMode ? "#8a8a8a" : "white";
        closeButton.innerHTML = "&times;";rding_completed,
        closeButton.onclick = function () {d_in,
            container.removeChild(innerContainer);eded,
        };

        const progressBar = document.createElement("div");
        progressBar.className = "progress";ta)
        progressBar.style.backgroundColor = "#e2e2e2";
        progressBar.style.position = "relative";
        progressBar.style.width = "100%";
        progressBar.style.height = "1.6rem";ed"}), 200
        progressBar.style.borderRadius = "2rem";
        progressBar.style.overflow = "hidden";
# Event Handlers
        const counter = document.createElement("p");
def handle_meeting_started(event_data):ute";
    meeting_id = event_data["payload"]["object"]["id"]
    host_email = event_data["payload"]["object"]["host_email"]
    print(f"🚀 Meeting {meeting_id} started by {host_email}")
        counter.style.transform = "translate(-50%, -50%)";
        counter.style.margin = 0;
def handle_meeting_ended(event_data):;
    meeting_id = event_data["payload"]["object"]["id"];
    print(f"📅 Meeting {meeting_id} ended")";
        progress.style.height = "100%";
        progress.style.width = "0%";
def handle_recording_completed(event_data):6093B5";
    recording_url = event_data["payload"]["object"]["recording_files"][0]["play_url"]
    print(f"🎥 New Recording Available: {recording_url}")
        progressBar.appendChild(progress);
        flexContainer.appendChild(title);
def handle_user_signed_in(event_data):eButton);
    user_email = event_data["payload"]["object"]["email"]
    print(f"👤 User Signed In: {user_email}")r);
        container.appendChild(innerContainer);
    };
def handle_rate_limit_exceeded(event_data):
    print("⚠️ API Rate Limit Exceeded! Consider throttling requests.")
        const innerContainer = document.getElementById("tel-downloader-progress-" + videoId);
# Run Flask Serveriner.querySelector("p.filename").innerText = fileName;
if __name__ == "__main__":= innerContainer.querySelector("div.progress");
    app.run(port=5000, debug=True)"p").innerText = progress + "%";
        progressBar.querySelector("div").style.width = progress + "%";
    };

    const completeProgress = (videoId) => {
        const progressBar = document.getElementById("tel-downloader-progress-" + videoId).querySelector("div.progress");
        progressBar.querySelector("p").innerText = "Completed";
        progressBar.querySelector("div").style.backgroundColor = "#B6C649";
        progressBar.querySelector("div").style.width = "100%";
    };

    const abortProgress = (videoId) => {
        const progressBar = document.getElementById("tel-downloader-progress-" + videoId).querySelector("div.progress");
        progressBar.querySelector("p").innerText = "Aborted";
        progressBar.querySelector("div").style.backgroundColor = "#D16666";
        progressBar.querySelector("div").style.width = "100%";
    };

    const tel_download_video = (url) => {
        let _blobs = [];
        let _next_offset = 0;
        let _total_size = null;
        let _file_extension = "mp4";

        const videoId = (Math.random() + 1).toString(36).substring(2, 10) + "_" + Date.now().toString();
        let fileName = hashCode(url).toString(36) + "." + _file_extension;

        try {
            const metadata = JSON.parse(decodeURIComponent(url.split("/").pop()));
            if (metadata.fileName) {
                fileName = metadata.fileName;
            }
        } catch (e) {
            // Invalid JSON string, pass extracting fileName
        }
        logger.info(`URL: ${url}`, fileName);

        const fetchNextPart = (_writable) => {
            fetch(url, {
                method: "GET",
                headers: {
                    Range: `bytes=${_next_offset}-`,
                },
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/117.0",
            })
                .then((res) => {
                    if (![200, 206].includes(res.status)) {
                        throw new Error("Non 200/206 response was received: " + res.status);
                    }
                    const mime = res.headers.get("Content-Type").split(";")[0];
                    if (!mime.startsWith("video/")) {
                        throw new Error("Get non video response with MIME type " + mime);
                    }
                    _file_extension = mime.split("/")[1];
                    fileName = fileName.substring(0, fileName.indexOf(".") + 1) + _file_extension;

                    const match = res.headers.get("Content-Range").match(contentRangeRegex);

                    const startOffset = parseInt(match[1]);
                    const endOffset = parseInt(match[2]);
                    const totalSize = parseInt(match[3]);

                    if (startOffset !== _next_offset) {
                        logger.error("Gap detected between responses.", fileName);
                        logger.info("Last offset: " + _next_offset, fileName);
                        logger.info("New start offset " + match[1], fileName);
                        throw "Gap detected between responses.";
                    }
                    if (_total_size && totalSize !== _total_size) {
                        logger.error("Total size differs", fileName);
                        throw "Total size differs";
                    }

                    _next_offset = endOffset + 1;
                    _total_size = totalSize;

                    logger.info(`Get response: ${res.headers.get("Content-Length")} bytes data from ${res.headers.get("Content-Range")}`, fileName);
                    logger.info(`Progress: ${((_next_offset * 100) / _total_size).toFixed(0)}%`, fileName);
                    updateProgress(videoId, fileName, ((_next_offset * 100) / _total_size).toFixed(0));
                    return res.blob();
                })
                .then((resBlob) => {
                    if (_writable !== null) {
                        _writable.write(resBlob).then(() => {});
                    } else {
                        _blobs.push(resBlob);
                    }
                })
                .then(() => {
                    if (!_total_size) {
                        throw new Error("_total_size is NULL");
                    }

                    if (_next_offset < _total_size) {
                        fetchNextPart(_writable);
                    } else {
                        if (_writable !== null) {
                            _writable.close().then(() => {
                                logger.info("Download finished", fileName);
                            });
                        } else {
                            save();
                        }
                        completeProgress(videoId);
                    }
                })
                .catch((reason) => {
                    logger.error(reason, fileName);
                    abortProgress(videoId);
                });
        };

        const save = () => {
            logger.info("Finish downloading blobs", fileName);
            logger.info("Concatenating blobs and downloading...", fileName);

            const blob = new Blob(_blobs, { type: "video/mp4" });
            const blobUrl = window.URL.createObjectURL(blob);

            logger.info("Final blob size: " + blob.size + " bytes", fileName);

            const a = document.createElement("a");
            document.body.appendChild(a);
            a.href = blobUrl;
            a.download = fileName;
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(blobUrl);

            logger.info("Download triggered", fileName);
        };

        const supportsFileSystemAccess = "showSaveFilePicker" in unsafeWindow && (() => {
            try {
                return unsafeWindow.self === unsafeWindow.top;
            } catch {
                return false;
            }
        })();
        if (supportsFileSystemAccess) {
            unsafeWindow.showSaveFilePicker({
                suggestedName: fileName,
            })
                .then((handle) => {
                    handle.createWritable()
                        .then((writable) => {
                            fetchNextPart(writable);
                            createProgressBar(videoId, fileName);
                        })
                        .catch((err) => {
                            console.error(err.name, err.message);
                        });
                })
                .catch((err) => {
                    if (err.name !== "AbortError") {
                        console.error(err.name, err.message);
                    }
                });
        } else {
            fetchNextPart(null);
            createProgressBar(videoId, fileName);
        }
    };

    const tel_download_audio = (url) => {
        let _blobs = [];
        let _next_offset = 0;
        let _total_size = null;
        const fileName = hashCode(url).toString(36) + ".ogg";

        const fetchNextPart = (_writable) => {
            fetch(url, {
                method: "GET",
                headers: {
                    Range: `bytes=${_next_offset}-`,
                },
            })
                .then((res) => {
                    if (res.status !== 206 && res.status !== 200) {
                        logger.error("Non 200/206 response was received: " + res.status, fileName);
                        return;
                    }

                    const mime = res.headers.get("Content-Type").split(";")[0];
                    if (!mime.startsWith("audio/")) {
                        logger.error("Get non audio response with MIME type " + mime, fileName);
                        throw "Get non audio response with MIME type " + mime;
                    }

                    try {
                        const match = res.headers.get("Content-Range").match(contentRangeRegex);

                        const startOffset = parseInt(match[1]);
                        const endOffset = parseInt(match[2]);
                        const totalSize = parseInt(match[3]);

                        if (startOffset !== _next_offset) {
                            logger.error("Gap detected between responses.");
                            logger.info("Last offset: " + _next_offset);
                            logger.info("New start offset " + match[1]);
                            throw "Gap detected between responses.";
                        }
                        if (_total_size && totalSize !== _total_size) {
                            logger.error("Total size differs");
                            throw "Total size differs";
                        }

                        _next_offset = endOffset + 1;
                        _total_size = totalSize;
                    } finally {
                        logger.info(`Get response: ${res.headers.get("Content-Length")} bytes data from ${res.headers.get("Content-Range")}`);
                        return res.blob();
                    }
                })
                .then((resBlob) => {
                    if (_writable !== null) {
                        _writable.write(resBlob).then(() => {});
                    } else {
                        _blobs.push(resBlob);
                    }
                })
                .then(() => {
                    if (_next_offset < _total_size) {
                        fetchNextPart(_writable);
                    } else {
                        if (_writable !== null) {
                            _writable.close().then(() => {
                                logger.info("Download finished", fileName);
                            });
                        } else {
                            save();
                        }
                    }
                })
                .catch((reason) => {
                    logger.error(reason, fileName);
                });
        };

        const save = () => {
            logger.info("Finish downloading blobs. Concatenating blobs and downloading...", fileName);

            let blob = new Blob(_blobs, { type: "audio/ogg" });
            const blobUrl = window.URL.createObjectURL(blob);

            logger.info("Final blob size in bytes: " + blob.size, fileName);

            blob = 0;

            const a = document.createElement("a");
            document.body.appendChild(a);
            a.href = blobUrl;
            a.download = fileName;
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(blobUrl);

            logger.info("Download triggered", fileName);
        };

        const supportsFileSystemAccess = "showSaveFilePicker" in unsafeWindow && (() => {
            try {
                return unsafeWindow.self === unsafeWindow.top;
            } catch {
                return false;
            }
        })();
        if (supportsFileSystemAccess) {
            unsafeWindow.showSaveFilePicker({
                suggestedName: fileName,
            })
                .then((handle) => {
                    handle.createWritable()
                        .then((writable) => {
                            fetchNextPart(writable);
                        })
                        .catch((err) => {
                            console.error(err.name, err.message);
                        });
                })
                .catch((err) => {
                    if (err.name !== "AbortError") {
                        console.error(err.name, err.message);
                    }
                });
        } else {
            fetchNextPart(null);
        }
    };

    const tel_download_image = (imageUrl) => {
        const fileName = (Math.random() + 1).toString(36).substring(2, 10) + ".jpeg"; // assume jpeg

        const a = document.createElement("a");
        document.body.appendChild(a);
        a.href = imageUrl;
        a.download = fileName;
        a.click();
        document.body.removeChild(a);

        logger.info("Download triggered", fileName);
    };

    const createDownloadButton = (iconClass, onClick) => {
        const downloadIcon = document.createElement("i");
        downloadIcon.className = iconClass;
        const downloadButton = document.createElement("button");
        downloadButton.className = "Button TkphaPyQ tiny translucent-white round tel-download";
        downloadButton.appendChild(downloadIcon);
        downloadButton.setAttribute("type", "button");
        downloadButton.setAttribute("title", "Download");
        downloadButton.setAttribute("aria-label", "Download");
        downloadButton.onclick = onClick;
        return downloadButton;
    };

    const addDownloadButtonToStory = (storiesContainer) => {
        const storyHeader = storiesContainer.querySelector(".GrsJNw3y") || storiesContainer.querySelector(".DropdownMenu").parentNode;
        if (storyHeader && !storyHeader.querySelector(".tel-download")) {
            storyHeader.insertBefore(createDownloadButton("icon icon-download", () => {
                const video = storiesContainer.querySelector("video");
                const videoSrc = video?.src || video?.currentSrc || video?.querySelector("source")?.src;
                if (videoSrc) {
                    tel_download_video(videoSrc);
                } else {
                    const images = storiesContainer.querySelectorAll("img.PVZ8TOWS");
                    if (images.length > 0) {
                        const imageSrc = images[images.length - 1]?.src;
                        if (imageSrc) tel_download_image(imageSrc);
                    }
                }
            }), storyHeader.querySelector("button"));
        }
    };

    const addDownloadButtonToMediaViewer = (mediaContainer, mediaViewerActions) => {
        const videoPlayer = mediaContainer.querySelector(".MediaViewerContent > .VideoPlayer");
        const img = mediaContainer.querySelector(".MediaViewerContent > div > img");

        const downloadButton = createDownloadButton("icon icon-download", () => {
            if (videoPlayer) {
                tel_download_video(videoPlayer.querySelector("video").currentSrc);
            } else if (img && img.src) {
                tel_download_image(img.src);
            }
        });

        if (videoPlayer) {
            const videoUrl = videoPlayer.querySelector("video").currentSrc;
            downloadButton.setAttribute("data-tel-download-url", videoUrl);

            const controls = videoPlayer.querySelector(".VideoPlayerControls");
            if (controls) {
                const buttons = controls.querySelector(".buttons");
                if (!buttons.querySelector("button.tel-download")) {
                    const spacer = buttons.querySelector(".spacer");
                    spacer.after(downloadButton);
                }
            }

            if (mediaViewerActions.querySelector("button.tel-download")) {
                const telDownloadButton = mediaViewerActions.querySelector("button.tel-download");
                if (mediaViewerActions.querySelectorAll('button[title="Download"]').length > 1) {
                    mediaViewerActions.querySelector("button.tel-download").remove();
                } else if (telDownloadButton.getAttribute("data-tel-download-url") !== videoUrl) {
                    telDownloadButton.onclick = () => {
                        tel_download_video(videoPlayer.querySelector("video").currentSrc);
                    };
                    telDownloadButton.setAttribute("data-tel-download-url", videoUrl);
                }
            } else if (!mediaViewerActions.querySelector('button[title="Download"]')) {
                mediaViewerActions.prepend(downloadButton);
            }
        } else if (img && img.src) {
            downloadButton.setAttribute("data-tel-download-url", img.src);

            if (mediaViewerActions.querySelector("button.tel-download")) {
                const telDownloadButton = mediaViewerActions.querySelector("button.tel-download");
                if (mediaViewerActions.querySelectorAll('button[title="Download"]').length > 1) {
                    mediaViewerActions.querySelector("button.tel-download").remove();
                } else if (telDownloadButton.getAttribute("data-tel-download-url") !== img.src) {
                    telDownloadButton.onclick = () => {
                        tel_download_image(img.src);
                    };
                    telDownloadButton.setAttribute("data-tel-download-url", img.src);
                }
            } else if (!mediaViewerActions.querySelector('button[title="Download"]')) {
                mediaViewerActions.prepend(downloadButton);
            }
        }
    };

    logger.info("Initialized");

    setInterval(() => {
        const storiesContainer = document.getElementById("StoryViewer");
        if (storiesContainer) {
            addDownloadButtonToStory(storiesContainer);
        }

        const mediaContainer = document.querySelector("#MediaViewer .MediaViewerSlide--active");
        const mediaViewerActions = document.querySelector("#MediaViewer .MediaViewerActions");
        if (mediaContainer && mediaViewerActions) {
            addDownloadButtonToMediaViewer(mediaContainer, mediaViewerActions);
        }
    }, REFRESH_DELAY);

    setInterval(() => {
        const pinnedAudio = document.body.querySelector(".pinned-audio");
        let dataMid;
        let downloadButtonPinnedAudio = document.body.querySelector("._tel_download_button_pinned_container") || document.createElement("button");
        if (pinnedAudio) {
            dataMid = pinnedAudio.getAttribute("data-mid");
            downloadButtonPinnedAudio.className = "btn-icon tgico-download _tel_download_button_pinned_container";
            downloadButtonPinnedAudio.innerHTML = `<span class="tgico button-icon">${DOWNLOAD_ICON}</span>`;
        }
        const audioElements = document.body.querySelectorAll("audio-element");
        audioElements.forEach((audioElement) => {
            const bubble = audioElement.closest(".bubble");
            if (!bubble || bubble.querySelector("._tel_download_button_pinned_container")) {
                return;
            }
            if (dataMid && downloadButtonPinnedAudio.getAttribute("data-mid") !== dataMid && audioElement.getAttribute("data-mid") === dataMid) {
                downloadButtonPinnedAudio.onclick = (e) => {
                    e.stopPropagation();
                    const link = audioElement.audio && audioElement.audio.getAttribute("src");
                    const isAudio = audioElement.audio && audioElement.audio instanceof HTMLAudioElement;
                    if (link) {
                        if (isAudio) {
                            tel_download_audio(link);
                        } else {
                            tel_download_video(link);
                        }
                    }
                };
                downloadButtonPinnedAudio.setAttribute("data-mid", dataMid);
                const link = audioElement.audio && audioElement.audio.getAttribute("src");
                if (link) {
                    pinnedAudio.querySelector(".pinned-container-wrapper-utils").appendChild(downloadButtonPinnedAudio);
                }
            }
        });

        const storiesContainer = document.getElementById("stories-viewer");
        if (storiesContainer) {
            const createDownloadButton = () => {
                const downloadButton = document.createElement("button");
                downloadButton.className = "btn-icon rp tel-download";
                downloadButton.innerHTML = `<span class="tgico">${DOWNLOAD_ICON}</span><div class="c-ripple"></div>`;
                downloadButton.setAttribute("type", "button");
                downloadButton.setAttribute("title", "Download");
                downloadButton.setAttribute("aria-label", "Download");
                downloadButton.onclick = () => {
                    const video = storiesContainer.querySelector("video.media-video");
                    const videoSrc = video?.src || video?.currentSrc || video?.querySelector("source")?.src;
                    if (videoSrc) {
                        tel_download_video(videoSrc);
                    } else {
                        const imageSrc = storiesContainer.querySelector("img.media-photo")?.src;
                        if (imageSrc) tel_download_image(imageSrc);
                    }
                };
                return downloadButton;
            };

            const storyHeader = storiesContainer.querySelector("[class^='_ViewerStoryHeaderRight']");
            if (storyHeader && !storyHeader.querySelector(".tel-download")) {
                storyHeader.prepend(createDownloadButton());
            }

            const storyFooter = storiesContainer.querySelector("[class^='_ViewerStoryFooterRight']");
            if (storyFooter && !storyFooter.querySelector(".tel-download")) {
                storyFooter.prepend(createDownloadButton());
            }
        }

        const mediaContainer = document.querySelector(".media-viewer-whole");
        if (!mediaContainer) return;
        const mediaAspecter = mediaContainer.querySelector(".media-viewer-movers .media-viewer-aspecter");
        const mediaButtons = mediaContainer.querySelector(".media-viewer-topbar .media-viewer-buttons");
        if (!mediaAspecter || !mediaButtons) return;

        const hiddenButtons = mediaButtons.querySelectorAll("button.btn-icon.hide");
        let onDownload = null;
        for (const btn of hiddenButtons) {
            btn.classList.remove("hide");
            if (btn.textContent === FORWARD_ICON) {
                btn.classList.add("tgico-forward");
            }
            if (btn.textContent === DOWNLOAD_ICON) {
                btn.classList.add("tgico-download");
                onDownload = () => {
                    btn.click();
                };
                logger.info("onDownload", onDownload);
            }
        }

        if (mediaAspecter.querySelector(".ckin__player")) {
            const controls = mediaAspecter.querySelector(".default__controls.ckin__controls");
            if (controls && !controls.querySelector(".tel-download")) {
                const brControls = controls.querySelector(".bottom-controls .right-controls");
                const downloadButton = document.createElement("button");
                downloadButton.className = "btn-icon default__button tgico-download tel-download";
                downloadButton.innerHTML = `<span class="tgico">${DOWNLOAD_ICON}</span>`;
                downloadButton.setAttribute("type", "button");
                downloadButton.setAttribute("title", "Download");
                downloadButton.setAttribute("aria-label", "Download");
                if (onDownload) {
                    downloadButton.onclick = onDownload;
                } else {
                    downloadButton.onclick = () => {
                        tel_download_video(mediaAspecter.querySelector("video").src);
                    };
                }
                brControls.prepend(downloadButton);
            }
        } else if (mediaAspecter.querySelector("video") && mediaAspecter.querySelector("video") && !mediaButtons.querySelector("button.btn-icon.tgico-download")) {
            const downloadButton = document.createElement("button");
            downloadButton.className = "btn-icon tgico-download tel-download";
            downloadButton.innerHTML = `<span class="tgico button-icon">${DOWNLOAD_ICON}</span>`;
            downloadButton.setAttribute("type", "button");
            downloadButton.setAttribute("title", "Download");
            downloadButton.setAttribute("aria-label", "Download");
            if (onDownload) {
                downloadButton.onclick = onDownload;
            } else {
                downloadButton.onclick = () => {
                    tel_download_video(mediaAspecter.querySelector("video").src);
                };
            }
            mediaButtons.prepend(downloadButton);
        } else if (!mediaButtons.querySelector("button.btn-icon.tgico-download")) {
            if (!mediaAspecter.querySelector("img.thumbnail") || !mediaAspecter.querySelector("img.thumbnail").src) {
                return;
            }
            const downloadButton = document.createElement("button");
            downloadButton.className = "btn-icon tgico-download tel-download";
            downloadButton.innerHTML = `<span class="tgico button-icon">${DOWNLOAD_ICON}</span>`;
            downloadButton.setAttribute("type", "button");
            downloadButton.setAttribute("title", "Download");
            downloadButton.setAttribute("aria-label", "Download");
            if (onDownload) {
                downloadButton.onclick = onDownload;
            } else {
                downloadButton.onclick = () => {
                    tel_download_image(mediaAspecter.querySelector("img.thumbnail").src);
                };
            }
            mediaButtons.prepend(downloadButton);
        }
    }, REFRESH_DELAY);

    (function setupProgressBar() {
        const body = document.querySelector("body");
        const container = document.createElement("div");
        container.id = "tel-downloader-progress-bar-container";
        container.style.position = "fixed";
        container.style.bottom = 0;
        container.style.right = 0;
        if (location.pathname.startsWith("/k/")) {
            container.style.zIndex = 4;
        } else {
            container.style.zIndex = 1600;
        }
        body.appendChild(container);
    })();

    logger.info("Completed script setup.");
})();