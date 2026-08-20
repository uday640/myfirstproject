from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from .models import key_storage

@login_required(login_url='login')
def upload_key(request):
    if request.method=="POST":
       files= request.FILES.getlist("uploadedFile")
       for f in files:
         datas=f.read()
         hasher=hashlib.sha256()
         hasher.update(datas)
         file_hash = hasher.hexdigest()
         model=key_storage.objects.filter(auther=request.user,hashcode=file_hash).first()
         if model:
          data=datas[16:]
          cipher= Cipher(
                      algorithms.AES(model.aes_key),
                      modes.CBC(datas[:16]),
                      backend=default_backend()
                      )
          decrypt=cipher.decryptor()
          decoded_data=decrypt.update(data)+decrypt.finalize()
          unpadder=padding.PKCS7(128).unpadder()
          unpadded_data=unpadder.update(decoded_data)+unpadder.finalize()
          model.files=unpadded_data
          model.save()
       return redirect('/get_file/?from=upload_key')
    return render(request, 'uploadfile.html')
    
    
    
def uploadmanage_key(request):
  if request.method=='POST':
    keys = key_storage.objects.filter(auther=request.user)
    for k in keys:
      chunks=[]
      chunks[0]=k[:len(k)/5]
      chunks[1]=k[len(k)/5:2*len(k)/5]
      chunks[2]=k[2*len(k)/5:3*len(k)/5]
      chunks[3]=k[3*len(k)/5:4*len(k)/5]
      chunks[4]=k[4*len(k)/5:len(k)]
      
      