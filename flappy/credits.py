import tkinter as tk

from Popup import Popup



def show_credits_popup(root):
    credits_content = """
    Programmer: Aditya Bhattacharjee
    
    Sponsor: New Horizon Public School
    
    Mentors: Laxmi Ma'am, Susan Ma'am
    
    Music Credit: Jurassic Park Theme Song
    
    Inspiration: Flappy Birds

    Github Repo: itabhijitb/augmented-flappy-python
    Email: email.adityab@gmail.com
    Made With: PyGame

    ────────────────────────────────────────────────────────────────────────────────
© 2024 Aditya Bhattacharjee. All rights reserved.

Licensed under the MIT License:
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
    """
    Popup(root, "Credits", credits_content)
    root.mainloop()

# Example of calling the Credits Popup
if __name__ == "__main__":
    root = tk.Tk()
    show_credits_popup(root)
