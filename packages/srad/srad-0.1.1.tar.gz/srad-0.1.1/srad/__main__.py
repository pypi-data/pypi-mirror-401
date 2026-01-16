import cv2
import os
from . import SRAD

def main():
    # Default to noisyImage.png in current directory if data/noisyImage.png not found
    f = 'data/noisyImage.png'
    if not os.path.exists(f):
        f = 'noisyImage.png'
        
    if os.path.exists(f):
        print(f"Processing {f}...")
        img = cv2.imread(f, cv2.IMREAD_GRAYSCALE)
        #np.savetxt("initial.csv", img, delimiter=",")

        iterationMaxStep, timeSize, decayFactor = 200,.05,1
        img = SRAD(img, iterationMaxStep, timeSize, decayFactor)

        cv2.imwrite('denoised.png',img)
        print("Saved denoised.png")
    else:
        print("Image file not found.")

if __name__ == "__main__":
    main()
