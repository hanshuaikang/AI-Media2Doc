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
    script.src = 'https://unpkg.com/@ffmpeg/ffmpeg@0.10.1/dist/ffmpeg.min.js'
    document.head.appendChild(script)
    
    await new Promise((resolve) => {
      script.onload = resolve
    })
    
    ffmpeg = FFmpeg.createFFmpeg({ 
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
