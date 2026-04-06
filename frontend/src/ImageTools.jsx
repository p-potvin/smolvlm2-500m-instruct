import React, { useRef, useState } from 'react';
import Cropper from 'react-easy-crop';
import AvatarEditor from 'react-avatar-editor';

export function ImageTools() {
  const [image, setImage] = useState(null);
  const [crop, setCrop] = useState({ x: 0, y: 0 });
  const [zoom, setZoom] = useState(1);
  const [croppedAreaPixels, setCroppedAreaPixels] = useState(null);
  const editorRef = useRef();

  const onSelectFile = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      const reader = new FileReader();
      reader.addEventListener('load', () => setImage(reader.result));
      reader.readAsDataURL(e.target.files[0]);
    }
  };

  return (
    <div className="p-4 bg-white dark:bg-gray-900 rounded shadow mb-8">
      <h2 className="text-xl font-bold mb-2">Photo Editing Tools</h2>
      <input type="file" accept="image/*" onChange={onSelectFile} className="mb-4" />
      {image && (
        <div className="flex flex-col md:flex-row gap-8">
          <div className="w-full md:w-1/2">
            <h3 className="font-semibold mb-2">Crop & Mask (react-easy-crop)</h3>
            <div className="relative w-full h-64 bg-gray-200 dark:bg-gray-800 rounded">
              <Cropper
                image={image}
                crop={crop}
                zoom={zoom}
                aspect={1}
                onCropChange={setCrop}
                onZoomChange={setZoom}
                onCropComplete={(_, croppedPixels) => setCroppedAreaPixels(croppedPixels)}
              />
            </div>
            <div className="flex items-center gap-2 mt-2">
              <label>Zoom</label>
              <input type="range" min={1} max={3} step={0.01} value={zoom} onChange={e => setZoom(Number(e.target.value))} />
            </div>
          </div>
          <div className="w-full md:w-1/2">
            <h3 className="font-semibold mb-2">Avatar Editor (react-avatar-editor)</h3>
            <AvatarEditor
              ref={editorRef}
              image={image}
              width={200}
              height={200}
              border={30}
              borderRadius={100}
              color={[255, 255, 255, 0.6]}
              scale={zoom}
              rotate={0}
            />
          </div>
        </div>
      )}
    </div>
  );
}