class RecorderProcessor extends AudioWorkletProcessor {
  constructor() {
    super();
    this.buffer = [];
    this.sampleRate = sampleRate;
    this.targetRate = 16000;

    this.port.onmessage = (event) => {
      if (event.data === "flush") {
        this.flush();
      }
    };
  }

  downsample(input, inputSampleRate, outputSampleRate) {
    const ratio = inputSampleRate / outputSampleRate;
    const newLength = Math.round(input.length / ratio);
    const result = new Float32Array(newLength);

    for (let i = 0; i < newLength; i++) {
      const index = i * ratio;
      const left = Math.floor(index);
      const right = Math.ceil(index);
      const frac = index - left;
      const leftVal = input[left] || 0;
      const rightVal = input[right] || leftVal;
      result[i] = leftVal + (rightVal - leftVal) * frac;
    }
    return result;
  }

  process(inputs) {
    const input = inputs[0][0];
    if (!input) return true;

    const pcm16k = this.downsample(input, this.sampleRate, this.targetRate);
    this.buffer.push(...pcm16k);

    // Gửi mỗi 0.5 giây: 16000Hz * 0.5 = 8000 samples
    if (this.buffer.length >= 8000) {
      const chunk = new Float32Array(this.buffer.splice(0, 8000));
      this.port.postMessage(chunk);
    }

    return true;
  }

  flush() {
    if (this.buffer.length > 0) {
      const chunk = new Float32Array(this.buffer);
      this.port.postMessage(chunk);
      this.buffer = [];
    }
  }
}

registerProcessor("recorder-processor", RecorderProcessor);