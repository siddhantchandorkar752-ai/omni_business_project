import os
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import transforms
from torch.utils.data import DataLoader
from PIL import Image
from gan_architecture import Generator, Discriminator

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def train_gan():
    transform = transforms.Compose([
        transforms.Resize((64, 64)),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])

    class DefectDataset(torch.utils.data.Dataset):
        def __init__(self, img_dir):
            self.img_dir = img_dir
            self.img_names = [f for f in os.listdir(img_dir) if f.endswith(('.png', '.jpg', '.jpeg', '.bmp'))]

        def __len__(self):
            return len(self.img_names)

        def __getitem__(self, idx):
            img_path = os.path.join(self.img_dir, self.img_names[idx])
            image = Image.open(img_path).convert('RGB')
            return transform(image), 0

    train_dir = "data/processed/train/images"
    dataset = DefectDataset(train_dir)
    dataloader = DataLoader(dataset, batch_size=8, shuffle=True)

    netG = Generator().to(device)
    netD = Discriminator().to(device)

    criterion = nn.BCELoss()
    optimizerD = optim.Adam(netD.parameters(), lr=0.0002, betas=(0.5, 0.999))
    optimizerG = optim.Adam(netG.parameters(), lr=0.0002, betas=(0.5, 0.999))

    print(f"Igniting GAN Training Engine on {device}...")

    for i, data in enumerate(dataloader):
        netD.zero_grad()
        real_cpu = data[0].to(device)
        b_size = real_cpu.size(0)
        label = torch.full((b_size,), 1.0, dtype=torch.float, device=device)
        
        output = netD(real_cpu).view(-1)
        errD_real = criterion(output, label)
        errD_real.backward()

        noise = torch.randn(b_size, 100, 1, 1, device=device)
        fake = netG(noise)
        label.fill_(0.0)
        
        output = netD(fake.detach()).view(-1)
        errD_fake = criterion(output, label)
        errD_fake.backward()
        optimizerD.step()

        netG.zero_grad()
        label.fill_(1.0)
        output = netD(fake).view(-1)
        errG = criterion(output, label)
        errG.backward()
        optimizerG.step()
        
        print(f"Batch {i+1}/{len(dataloader)} | Discriminator Loss: {errD_real.item()+errD_fake.item():.4f} | Generator Loss: {errG.item():.4f}")
        
        if i >= 5:
            break

    torch.save(netG.state_dict(), "models/gan_checkpoints/generator_v1.pth")
    torch.save(netD.state_dict(), "models/gan_checkpoints/discriminator_v1.pth")
    print("GAN Training Test Epoch Complete. Checkpoints saved successfully.")

if __name__ == '__main__':
    train_gan()