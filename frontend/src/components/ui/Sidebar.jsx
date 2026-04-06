import React from 'react';

export function Sidebar({ categories, onSelect, selected }) {
  return (
    <aside className="w-full md:w-64 bg-vault-50 dark:bg-vault-900 border-b md:border-b-0 md:border-r border-vault-200 dark:border-vault-700 p-4 font-vault flex-shrink-0">
      <h3 className="text-lg font-bold mb-4 text-vault-800 dark:text-vault-100">Categories</h3>
      <ul className="space-y-2 flex md:block flex-row overflow-x-auto">
        {categories.map((cat) => (
          <li key={cat} className="mr-2 md:mr-0">
            <button
              className={`w-full text-left px-2 py-1 rounded ${selected === cat ? 'bg-vault-200 dark:bg-vault-800 font-semibold text-vault-900 dark:text-vault-100' : 'text-vault-700 dark:text-vault-300'}`}
              onClick={() => onSelect(cat)}
            >
              {cat}
            </button>
          </li>
        ))}
      </ul>
    </aside>
  );
}
