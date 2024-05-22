import base64

# This helped me make image pngs to base64 ascii,
# so the code for the images could be included in the executable
def convert_image_to_code(image_path):
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('ascii')
    return f"b'{encoded_image}'"

if __name__ == "__main__":
    image_paths = [
        "images/agent.png", "images/barrier.png", 
        "images/bomb_exploding.png", "images/bomb.png", 
        "images/bullet.png", "images/cannon.png", 
        "images/enemy.png", "images/heart.png", 
        "images/lightning.png", "images/poison.png", 
        "images/shield.png", "images/zombie.png",
        "images/star.png", "images/saiyan.png",
        "images/bullet_gold.png", "images/honey.png",
        "images/firecracker/firecracker_u.png", "images/firecracker/firecracker_l.png",
        "images/firecracker/firecracker_r.png", "images/firecracker/firecracker_d.png",
        "images/firework.png"
    ]
    
    for image_path in image_paths:
        image_code = convert_image_to_code(image_path)
        print(f"{image_path}: {image_code}")
