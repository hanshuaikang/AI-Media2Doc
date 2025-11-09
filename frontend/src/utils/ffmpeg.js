let ffmpeg = null
let ffmpegLoaded = false
let ffmpegLoading = false
let cachedVideoFile = null // 新增：缓存当前视频文件名

export const loadFFmpeg = async () => {
  if (ffmpegLoaded) return ffmpeg

  if (ffmpegLoading) {
    return new Promise((resolve) => {
      const checkLoaded = setInterval(() => {
        if (ffmpegLoaded) {
          clearInterval(checkLoaded)
          resolve(ffmpeg)
        }
      }, 100)
    })
  }

  ffmpegLoading = true

  try {
    const script = document.createElement('script')
    script.src = '/assets/ffmpeg/ffmpeg.min.js'

    document.head.appendChild(script)

    await new Promise((resolve) => {
      script.onload = resolve
    })

    ffmpeg = FFmpeg.createFFmpeg({
      corePath: '/assets/ffmpeg/ffmpeg-core.js',
      log: true,
      progress: ({ ratio }) => {
        // 进度回调
      }
    })

    await ffmpeg.load()
    ffmpegLoaded = true
    return ffmpeg

  } catch (error) {
    console.error('FFmpeg 加载错误:', error)
    throw error
  } finally {
    ffmpegLoading = false
  }
}

export const extractAudio = async (videoData) => {
  try {
    ffmpeg.FS('writeFile', 'input_video.mp4', videoData)
    await ffmpeg.run('-i', 'input_video.mp4', '-q:a', '0', '-map', 'a', 'output_audio.mp3')
    return ffmpeg.FS('readFile', 'output_audio.mp3')
  } catch (error) {
    console.error('音频提取失败:', error)
    throw error
  }
}

/**
 * 预处理视频文件，缓存到FFmpeg文件系统中
 * @param {Uint8Array} videoData 视频数据
 * @returns {string} 缓存的文件名
 */
export const prepareVideoForCapture = async (videoData) => {
  try {
    if (cachedVideoFile) {
      // 清理之前的缓存文件
      try {
        ffmpeg.FS('unlink', cachedVideoFile)
      } catch (e) {
        console.warn('清理旧缓存文件失败:', e)
      }
    }

    const timestamp = Date.now()
    cachedVideoFile = `cached_video_${timestamp}.mp4`

    ffmpeg.FS('writeFile', cachedVideoFile, videoData)

    return cachedVideoFile
  } catch (error) {
    console.error('视频预处理失败:', error)
    throw error
  }
}

/**
 * 自定义截图错误类
 */
class CaptureError extends Error {
  constructor(message, code, timeInSeconds = null, videoDuration = null) {
    super(message)
    this.name = 'CaptureError'
    this.code = code
    this.timeInSeconds = timeInSeconds
    this.videoDuration = videoDuration
  }
}

/**
 * 读取“视频 API 截图大小阈值”（单位MB），来源于其他设置的本地存储
 * 默认 100MB
 */
function getVideoApiMaxSizeMB() {
  try {
    const v = localStorage.getItem('videoApiMaxSizeMB')
    if (v) {
      const n = parseInt(v)
      if (!isNaN(n) && n > 0) return n
    }
  } catch {}
  return 200
}

function getVideoApiThresholdBytes() {
  return getVideoApiMaxSizeMB() * 1024 * 1024
}

/**
 * 使用HTML5 Video API快速截图（适用于浏览器支持的格式）
 * @param {Blob} videoBlob 视频文件Blob
 * @param {number} timeInSeconds 截图时间点（秒）
 * @returns {Promise<Uint8Array>} 截图数据
 */
export const captureFrameWithVideoAPI = async (videoBlob, timeInSeconds) => {
  // 对于大文件（>50MB），直接抛出错误让其使用FFmpeg
  const MAX_SIZE_FOR_VIDEO_API = getVideoApiThresholdBytes() // 来自设置，默认 100MB
  if (videoBlob.size > MAX_SIZE_FOR_VIDEO_API) {
    throw new Error(`文件过大 (${Math.round(videoBlob.size / 1024 / 1024)}MB)，超过阈值，无法使用浏览器截图。请在“设置 > 其他设置”调整阈值或减小文件大小。`)
  }

  console.log(`开始使用Video API截图，文件大小: ${Math.round(videoBlob.size / 1024 / 1024)}MB，时间点: ${timeInSeconds}s`)

  return new Promise((resolve, reject) => {
    const video = document.createElement('video')
    const canvas = document.createElement('canvas')
    const ctx = canvas.getContext('2d')
    let isResolved = false

    const cleanup = () => {
      console.log('清理Video API资源')
      if (video.src) {
        URL.revokeObjectURL(video.src)
      }
      video.src = ''
      video.load() // 释放内存
    }

    video.addEventListener('loadedmetadata', () => {
      if (isResolved) return

      console.log(`视频元数据加载完成: 尺寸 ${video.videoWidth}x${video.videoHeight}, 时长 ${video.duration}s`)

      // 检查视频时长，如果timeInSeconds超出范围则报错
      if (timeInSeconds > video.duration) {
        console.error(`截图时间点超出范围: ${timeInSeconds}s > ${video.duration}s`)
        isResolved = true
        cleanup()
        reject(new CaptureError(
          `截图时间点 ${timeInSeconds}s 超出视频时长 ${video.duration}s`,
          'TIME_OUT_OF_RANGE',
          timeInSeconds,
          video.duration
        ))
        return
      }

      // 设置画布尺寸，限制最大尺寸以提高性能
      const maxWidth = 800
      const maxHeight = 600
      const scale = Math.min(maxWidth / video.videoWidth, maxHeight / video.videoHeight, 1)

      canvas.width = video.videoWidth * scale
      canvas.height = video.videoHeight * scale

      console.log(`Video API截图: ${video.videoWidth}x${video.videoHeight} -> ${canvas.width}x${canvas.height}`)
    })

    video.addEventListener('seeked', () => {
      if (isResolved) return

      console.log(`视频跳转到 ${timeInSeconds}s 完成，开始截图`)

      try {
        // 绘制当前帧到画布
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height)
        console.log('帧绘制到画布完成')

        // 转换为Blob然后到Uint8Array
        canvas.toBlob((blob) => {
          if (isResolved) return

          if (blob) {
            console.log(`截图Blob生成成功，大小: ${Math.round(blob.size / 1024)}KB`)
            const reader = new FileReader()
            reader.onload = () => {
              if (!isResolved) {
                console.log('截图数据转换为Uint8Array成功')
                isResolved = true
                cleanup()
                const arrayBuffer = reader.result
                const uint8Array = new Uint8Array(arrayBuffer)
                resolve(uint8Array)
              }
            }
            reader.onerror = () => {
              if (!isResolved) {
                console.error('FileReader转换失败')
                isResolved = true
                cleanup()
                reject(new Error('FileReader转换失败'))
              }
            }
            reader.readAsArrayBuffer(blob)
          } else {
            if (!isResolved) {
              console.error('Canvas转换为Blob失败')
              isResolved = true
              cleanup()
              reject(new Error('Canvas转换失败'))
            }
          }
        }, 'image/jpeg', 0.85)
      } catch (error) {
        if (!isResolved) {
          console.error('截图过程发生错误:', error)
          isResolved = true
          cleanup()
          reject(error)
        }
      }
    })

    video.addEventListener('error', (e) => {
      if (!isResolved) {
        console.error('视频加载错误:', e)
        isResolved = true
        cleanup()
        reject(new Error(`视频加载失败: ${e.message || '未知错误'}`))
      }
    })

    video.addEventListener('loadstart', () => {
      console.log('开始加载视频数据')
    })

    video.addEventListener('canplay', () => {
      console.log('视频可以开始播放')
    })

    // 设置视频属性以优化性能
    video.preload = 'metadata' // 只预加载元数据
    video.muted = true
    video.playsInline = true

    try {
      // 设置视频源并跳转到指定时间
      console.log('创建视频对象URL并设置时间点')
      video.src = URL.createObjectURL(videoBlob)
      video.currentTime = timeInSeconds
    } catch (error) {
      if (!isResolved) {
        console.error('设置视频源失败:', error)
        isResolved = true
        cleanup()
        reject(error)
      }
    }
  })
}

export const captureVideoFrame = async (videoData, timeInSeconds) => {
  try {
    // 始终使用 HTML5 Video API 进行截图，不再回退到 FFmpeg
    const videoSize = videoData.length
    console.log(`视频文件大小: ${Math.round(videoSize / 1024 / 1024)}MB`)
    console.log('使用 HTML5 Video API 截图')

    const videoBlob = new Blob([videoData], { type: 'video/mp4' })
    return await captureFrameWithVideoAPI(videoBlob, timeInSeconds)
  } catch (error) {
    console.error('视频截图失败:', error)
    throw error
  }
}

/**
 * 清理缓存的视频文件
 */
export const cleanupVideoCache = () => {
  if (cachedVideoFile) {
    try {
      ffmpeg.FS('unlink', cachedVideoFile)
    } catch (e) {
      // 忽略清理错误
    }
    cachedVideoFile = null
  }
}


export const frameToBase64 = (frameData) => {
  try {
    // 将Uint8Array转换为base64
    const binary = Array.from(frameData, byte => String.fromCharCode(byte)).join('')
    const base64 = btoa(binary)
    return `data:image/jpeg;base64,${base64}`
  } catch (error) {
    console.error('转换base64失败:', error)
    throw error
  }
}
