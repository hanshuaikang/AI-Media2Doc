let ffmpeg = null
let ffmpegLoaded = false
let ffmpegLoading = false

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

export const captureVideoFrame = async (videoData, timeInSeconds) => {
  try {
    const inputFile = 'input_video.mp4'
    const outputFile = `frame_${timeInSeconds}.jpg`

    // 写入视频文件
    ffmpeg.FS('writeFile', inputFile, videoData)

    // 使用FFmpeg截取指定时间的帧
    await ffmpeg.run(
      '-i', inputFile,
      '-ss', timeInSeconds.toString(),
      '-vframes', '1',
      '-q:v', '2',
      outputFile
    )

    // 读取截图文件
    const frameData = ffmpeg.FS('readFile', outputFile)

    // 清理临时文件
    try {
      ffmpeg.FS('unlink', inputFile)
      ffmpeg.FS('unlink', outputFile)
    } catch (e) {
      // 忽略清理错误
    }

    return frameData
  } catch (error) {
    console.error('视频截图失败:', error)
    throw error
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
