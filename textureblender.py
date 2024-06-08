import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np

def blend_textures(diffuse1_path, normal1_path, specular1_path, diffuse2_path, normal2_path, specular2_path, blend_texture_path, blend_path):
    diffuse1 = Image.open(diffuse1_path)
    normal1 = Image.open(normal1_path)
    specular1 = Image.open(specular1_path)
    diffuse2 = Image.open(diffuse2_path)
    normal2 = Image.open(normal2_path)
    specular2 = Image.open(specular2_path)
    blend_texture = Image.open(blend_texture_path)
    assert diffuse1.size == normal1.size == specular1.size == diffuse2.size == normal2.size == specular2.size == blend_texture.size, "Textures must have the same dimensions"
    
    # Convert images to numpy arrays for faster processing
    diffuse1_np = np.array(diffuse1)
    normal1_np = np.array(normal1)
    specular1_np = np.array(specular1)
    diffuse2_np = np.array(diffuse2)
    normal2_np = np.array(normal2)
    specular2_np = np.array(specular2)
    blend_texture_np = np.array(blend_texture)
    
    # Blend textures
    blended_diffuse_np, blended_normal_np, blended_specular_np = custom_blend(diffuse1_np, normal1_np, specular1_np, diffuse2_np, normal2_np, specular2_np, blend_texture_np)
    
    # Convert numpy arrays back to images
    blended_diffuse = Image.fromarray(blended_diffuse_np)
    blended_normal = Image.fromarray(blended_normal_np)
    blended_specular = Image.fromarray(blended_specular_np)
    
    # Save the blended textures
    blended_diffuse.save(blend_path + "_diffuse.png")
    blended_normal.save(blend_path + "_normal.png")
    blended_specular.save(blend_path + "_specular.png")

def custom_blend(diffuse1_np, normal1_np, specular1_np, diffuse2_np, normal2_np, specular2_np, blend_texture_np):
    # Create arrays to store the blended textures
    blended_diffuse_np = np.zeros_like(diffuse1_np)
    blended_normal_np = np.zeros_like(normal1_np)
    blended_specular_np = np.zeros_like(specular1_np)
    
    # Iterate over each pixel
    for i in range(diffuse1_np.shape[0]):
        for j in range(diffuse1_np.shape[1]):
            # Get the pixel values of both diffuse textures, normal textures, specular textures, and blend texture
            diffuse_pixel1 = diffuse1_np[i, j]
            normal_pixel1 = normal1_np[i, j]
            specular_pixel1 = specular1_np[i, j]
            diffuse_pixel2 = diffuse2_np[i, j]
            normal_pixel2 = normal2_np[i, j]
            specular_pixel2 = specular2_np[i, j]
            blend_pixel = blend_texture_np[i, j]
            
            # Blend the textures based on blend texture pixel value
            if np.all(blend_pixel == [0, 0, 0]):  # If blend pixel is black
                blended_diffuse_np[i, j] = diffuse_pixel1
                blended_normal_np[i, j] = normal_pixel1
                blended_specular_np[i, j] = specular_pixel1
            elif np.all(blend_pixel == [255, 0, 0]):  # If blend pixel is red
                blended_diffuse_np[i, j] = diffuse_pixel2
                blended_normal_np[i, j] = normal_pixel2
                blended_specular_np[i, j] = specular_pixel2
            else:
                # Calculate blend factor based on red channel intensity
                blend_factor = blend_pixel[0] / 255.0
                # Blend the textures
                blended_diffuse_np[i, j] = (1 - blend_factor) * diffuse_pixel1 + blend_factor * diffuse_pixel2
                blended_normal_np[i, j] = (1 - blend_factor) * normal_pixel1 + blend_factor * normal_pixel2
                blended_specular_np[i, j] = (1 - blend_factor) * specular_pixel1 + blend_factor * specular_pixel2
                
    return blended_diffuse_np, blended_normal_np, blended_specular_np

def open_file(entry):
    file_path = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, file_path)

def update_blend():
    blend_textures(diffuse1_entry.get(), normal1_entry.get(), specular1_entry.get(), diffuse2_entry.get(), normal2_entry.get(), specular2_entry.get(), blend_texture_entry.get(), blend_path_entry.get())
    show_image(blend_path_entry.get() + "_diffuse.png")

def show_image(image_path):
    image = Image.open(image_path)
    photo = ImageTk.PhotoImage(image)
    label.config(image=photo)
    label.image = photo

# Create the main window
root = tk.Tk()
root.title("Texture Blending")

# Create and place widgets
tk.Label(root, text="Diffuse 1:").grid(row=0, column=0, padx=5, pady=5)
diffuse1_entry = tk.Entry(root, width=50)
diffuse1_entry.grid(row=0, column=1, padx=5, pady=5)
tk.Button(root, text="Browse", command=lambda: open_file(diffuse1_entry)).grid(row=0, column=2, padx=5, pady=5)

tk.Label(root, text="Normal 1:").grid(row=1, column=0, padx=5, pady=5)
normal1_entry = tk.Entry(root, width=50)
normal1_entry.grid(row=1, column=1, padx=5, pady=5)
tk.Button(root, text="Browse", command=lambda: open_file(normal1_entry)).grid(row=1, column=2, padx=5, pady=5)

tk.Label(root, text="Specular 1:").grid(row=2, column=0, padx=5, pady=5)
specular1_entry = tk.Entry(root, width=50)
specular1_entry.grid(row=2, column=1, padx=5, pady=5)
tk.Button(root, text="Browse", command=lambda: open_file(specular1_entry)).grid(row=2, column=2, padx=5, pady=5)

tk.Label(root, text="Diffuse 2:").grid(row=3, column=0, padx=5, pady=5)
diffuse2_entry = tk.Entry(root, width=50)
diffuse2_entry.grid(row=3, column=1, padx=5, pady=5)
tk.Button(root, text="Browse", command=lambda: open_file(diffuse2_entry)).grid(row=3, column=2, padx=5, pady=5)

tk.Label(root, text="Normal 2:").grid(row=4, column=0, padx=5, pady=5)
normal2_entry = tk.Entry(root, width=50)
normal2_entry.grid(row=4, column=1, padx=5, pady=5)
tk.Button(root, text="Browse", command=lambda: open_file(normal2_entry)).grid(row=4, column=2, padx=5, pady=5)

tk.Label(root, text="Specular 2:").grid(row=5, column=0, padx=5, pady=5)
specular2_entry = tk.Entry(root, width=50)
specular2_entry.grid(row=5, column=1, padx=5, pady=5)
tk.Button(root, text="Browse", command=lambda: open_file(specular2_entry)).grid(row=5, column=2, padx=5, pady=5)

tk.Label(root, text="Blend Texture:").grid(row=6, column=0, padx=5, pady=5)
blend_texture_entry = tk.Entry(root, width=50)
blend_texture_entry.grid(row=6, column=1, padx=5, pady=5)
tk.Button(root, text="Browse", command=lambda: open_file(blend_texture_entry)).grid(row=6, column=2, padx=5, pady=5)

tk.Label(root, text="Blended Texture Prefix:").grid(row=7, column=0, padx=5, pady=5)
blend_path_entry = tk.Entry(root, width=50)
blend_path_entry.grid(row=7, column=1, padx=5, pady=5)

tk.Button(root, text="Blend", command=update_blend).grid(row=8, column=1, padx=5, pady=5)

label = tk.Label(root)
label.grid(row=9, column=0, columnspan=3)

# Run the application
root.mainloop()
