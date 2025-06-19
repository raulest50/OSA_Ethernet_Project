// File selector functionality
window.dash_clientside = Object.assign({}, window.dash_clientside, {
    file_selector: {
        /**
         * Setup the hidden file inputs for folder and file selection
         * This is called once when the page loads
         */
        setupFolderPicker: function() {
            // Create hidden folder input if it doesn't exist
            if (!document.getElementById('hidden-folder-input')) {
                const input = document.createElement('input');
                input.type = 'file';
                input.id = 'hidden-folder-input';
                input.setAttribute('webkitdirectory', '');
                input.setAttribute('directory', '');
                input.style.display = 'none';
                document.body.appendChild(input);
            }

            // Create hidden file input for CSV files if it doesn't exist
            if (!document.getElementById('hidden-file-input')) {
                const input = document.createElement('input');
                input.type = 'file';
                input.id = 'hidden-file-input';
                input.accept = '.csv';
                input.style.display = 'none';
                document.body.appendChild(input);
            }

            return true;
        },

        /**
         * Open a native folder picker dialog
         * 
         * @param {number} n_clicks - Number of button clicks
         * @returns {string} - Selected folder path or null if cancelled
         */
        openFolderPicker: async function(n_clicks) {
            if (!n_clicks) return null;

            try {
                // Check if File System Access API is supported
                if ('showDirectoryPicker' in window) {
                    // Modern browsers with File System Access API
                    const directoryHandle = await window.showDirectoryPicker();

                    // Try to get a better path representation if possible
                    let path = directoryHandle.name;

                    // For some browsers, we might be able to get more path information
                    if (directoryHandle.path) {
                        path = directoryHandle.path;
                    }

                    return path;
                } else {
                    // Fallback for browsers without File System Access API
                    // Use the hidden file input
                    const input = document.getElementById('hidden-folder-input');
                    if (input) {
                        // Create a promise that resolves when the file input changes
                        const promise = new Promise((resolve) => {
                            const handleChange = function() {
                                input.removeEventListener('change', handleChange);

                                if (input.files.length > 0) {
                                    // Get folder path from the first file
                                    const folderPath = input.files[0].webkitRelativePath.split('/')[0];
                                    resolve(folderPath);
                                } else {
                                    resolve(null);
                                }
                            };

                            input.addEventListener('change', handleChange);
                            input.click();

                            // Also handle cancel by adding a click event to the document
                            setTimeout(() => {
                                const handleCancel = function() {
                                    document.removeEventListener('click', handleCancel);
                                    input.removeEventListener('change', handleChange);
                                    resolve(null);
                                };
                                document.addEventListener('click', handleCancel);
                            }, 100);
                        });

                        return await promise;
                    } else {
                        alert("Su navegador no soporta la selección nativa de carpetas. Por favor, ingrese la ruta manualmente.");
                        return null;
                    }
                }
            } catch (error) {
                console.error("Error selecting folder:", error);
                return null;
            }
        },

        /**
         * Open a file picker dialog for CSV files
         * 
         * @param {number} n_clicks - Number of button clicks
         * @returns {Object} - Object containing file path and content, or null if cancelled
         */
        openFilePicker: async function(n_clicks) {
            if (!n_clicks) return null;

            try {
                // Check if File System Access API is supported
                if ('showOpenFilePicker' in window) {
                    // Modern browsers with File System Access API
                    const opts = {
                        types: [{
                            description: 'CSV Files',
                            accept: {
                                'text/csv': ['.csv'],
                            }
                        }],
                        excludeAcceptAllOption: false,
                        multiple: false
                    };

                    const [fileHandle] = await window.showOpenFilePicker(opts);
                    const file = await fileHandle.getFile();
                    const content = await file.text();

                    return {
                        name: file.name,
                        path: fileHandle.name,
                        content: content
                    };
                } else {
                    // Fallback for browsers without File System Access API
                    // Use a hidden file input
                    const input = document.getElementById('hidden-file-input');
                    if (input) {
                        // Create a promise that resolves when the file input changes
                        const promise = new Promise((resolve) => {
                            const handleChange = function() {
                                input.removeEventListener('change', handleChange);

                                if (input.files.length > 0) {
                                    const file = input.files[0];
                                    const reader = new FileReader();

                                    reader.onload = function(e) {
                                        resolve({
                                            name: file.name,
                                            path: file.name,
                                            content: e.target.result
                                        });
                                    };

                                    reader.readAsText(file);
                                } else {
                                    resolve(null);
                                }
                            };

                            input.addEventListener('change', handleChange);
                            input.click();

                            // Handle cancel
                            setTimeout(() => {
                                const handleCancel = function() {
                                    document.removeEventListener('click', handleCancel);
                                    input.removeEventListener('change', handleChange);
                                    resolve(null);
                                };
                                document.addEventListener('click', handleCancel);
                            }, 100);
                        });

                        return await promise;
                    } else {
                        alert("Su navegador no soporta la selección nativa de archivos. Por favor, intente con otro navegador.");
                        return null;
                    }
                }
            } catch (error) {
                console.error("Error selecting file:", error);
                return null;
            }
        }
    }
});
