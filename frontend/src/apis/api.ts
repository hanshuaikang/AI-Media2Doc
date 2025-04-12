export const uploadFile = async (url: string, file: Blob, onProgress?: (progress: number) => void) => {
  const xhr = new XMLHttpRequest()
  
  return new Promise((resolve, reject) => {
    xhr.upload.onprogress = (event) => {
      if (event.lengthComputable && onProgress) {
        const percentComplete = Math.round((event.loaded / event.total) * 100)
        onProgress(percentComplete)
      }
    }
    
    xhr.onloadend = () => {
      if (xhr.status >= 200 && xhr.status < 300) {
        resolve(xhr.response)
      } else {
        reject(new Error(`Upload failed: ${xhr.status}`))
      }
    }
    
    xhr.onerror = () => reject(new Error('Upload failed'))
    
    xhr.open('PUT', url)
    xhr.send(file)
  })
}

