import React, { useState } from 'react';

export function ImageCaptioning() {
  const [image, setImage] = useState(null);
  const [caption, setCaption] = useState('');
  const [tags, setTags] = useState([]);
  const [loading, setLoading] = useState(false);

  const onSelectFile = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      const reader = new FileReader();
      reader.addEventListener('load', () => setImage(reader.result));
      reader.readAsDataURL(e.target.files[0]);
    }
  };

  // Placeholder for backend call
  const handleCaption = async () => {
    setLoading(true);
    setTimeout(() => {
      setCaption('A placeholder caption for the uploaded image.');
      setTags(['tag1', 'tag2', 'tag3']);
      setLoading(false);
    }, 1200);
  };

  return (
    <div className="p-4 bg-white dark:bg-gray-900 rounded shadow mb-8">
      <h2 className="text-xl font-bold mb-2">Image Captioning & Tagging</h2>
      <input type="file" accept="image/*" onChange={onSelectFile} className="mb-4" />
      {image && (
        <div className="flex flex-col md:flex-row gap-8">
          <div className="w-full md:w-1/2 flex flex-col items-center">
            <img src={image} alt="preview" className="max-h-48 rounded border mb-2" />
            <button
              className="px-4 py-2 rounded bg-vault-900 dark:bg-vault-100 text-white dark:text-vault-900 font-bold shadow hover:bg-vault-800 dark:hover:bg-vault-200"
              onClick={handleCaption}
              disabled={loading}
            >
              {loading ? 'Analyzing...' : 'Generate Caption & Tags'}
            </button>
          </div>
          <div className="w-full md:w-1/2">
            <div className="mb-2">
              <label className="block text-sm font-medium mb-1">Caption:</label>
              <div className="p-2 bg-gray-100 dark:bg-gray-800 rounded min-h-[2.5rem]">{caption}</div>
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Tags:</label>
              <div className="flex flex-wrap gap-2">
                {tags.map((tag, i) => (
                  <span key={i} className="px-2 py-0.5 text-xs rounded bg-vault-100 dark:bg-vault-800 text-vault-700 dark:text-vault-200 border border-vault-200 dark:border-vault-700">{tag}</span>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
