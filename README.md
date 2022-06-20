# rclone-combine-rename
Rename aliases used in the combine remote to unique ones (if you have multiple google accounts). \
If you have a crypted SharedDrive/TeamDrive, you will need to change the names of the crypted alias remotes to crypted ones. (See 5.)


Dependencies:
```
pyperclip
argparse
```

## Parameters:
```
--clipboard                    Take the combine config from the clipboard instead from the --file
--cryptfile <path_to_file>     Path to a file with one or 2 passwords, one password in each line
```


## Usage & example:

My Example config:
```
[Linux ISOs]
type = alias
remote = google_drive_acc,team_drive=0A...,root_folder_id=:

[Crypted Holiday Images]
type = alias
remote = google_drive_acc,team_drive=0A...,root_folder_id=:

[AllDrives]
type = combine
upstreams = "Linux ISOs=Linux ISOs:" "Crypted Holiday Images=Crypted Holiday Images:"

```


1. Get the combine config with the following command (replace drive_remote with the name of your remote): \
`rclone backend drives -o config <drive_remote>:`
2. Copy the config in your clipboard or write it into input.txt
3. Open rename.json with a text editor 
4. Write the names of the alias remotes as keys and the new name as values (see #renamejson-example)
5. (optional) If you have crypted files and want to access them, you have to do 2 things: \
  5.1 Get the 1 or 2 passwords for the crypt and write it into "crypt.txt" \
  5.2 Get the crypted names for your drive. \
      You can get these by already having a crypt drive with these passwords and using the following command: \
      `rclone backend encode <crypt_remote>: "unencrypted name"` \
      This will output a crypted name which you can use in the rename.json file.
6. Run the combine.py with the coresponding parameters (`--clipboard` if you didn't write it in input.txt) (`--cryptfile crypt.txt` if you added passwords)
7. Copy the contents of output.txt into the rclone config file. (Find out the location with `rclone config file`)


# Rename.json example
`omg67bhn93d4r67bg8df43r67hgbfd43r6h7gdf34rh6g7` is a crypted name for `[Images] Holidays`
```
{
  "Linux ISOs": "[ISOs] Linux",
  "Crypted Holiday Images": "omg67bhn93d4r67bg8df43r67hgbfd43r6h7gdf34rh6g7"
}
```

# Output config
```
[root_google_drive_acc]
type = alias
remote = google_drive_acc,team_drive=,root_folder_id=root:

[Linux ISOs_google_drive_acc]
type = alias
remote = google_drive_acc,team_drive=0A...,root_folder_id=:

[Crypted Holiday Images_google_drive_acc]
type = alias
remote = google_drive_acc,team_drive=0A...,root_folder_id=:

[google_drive_acc_all]
type = combine
upstreams = "[_Root] Root=root_google_drive_acc:" "[ISOs] Linux=Linux ISOs_google_drive_acc:" "omg67bhn93d4r67bg8df43r67hgbfd43r6h7gdf34rh6g7=Crypted Holiday Images_google_drive_acc:"

[google_drive_acc_all_crypt]
type = crypt
remote = google_drive_acc_all:
password = ertvgvetrhgrz
password2 = vterhgvthervterhg```
