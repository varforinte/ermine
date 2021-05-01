;;; ermine.el --- Evaluate MEL and Python in Maya

;; Copyright (C) 2020 craig

;; This program is free software: you can redistribute it and/or modify
;; it under the terms of the GNU General Public License as published by
;; the Free Software Foundation, either version 3 of the License, or
;; (at your option) any later version.

;; This program is distributed in the hope that it will be useful,
;; but WITHOUT ANY WARRANTY; without even the implied warranty of
;; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;; GNU General Public License for more details.

;; You should have received a copy of the GNU General Public License
;; along with this program.  If not, see <https://www.gnu.org/licenses/>.


(require 'python)
(require 'comint)

(defvar ermine-mel-comint-buffer nil)

(defun ermine-python-path ()
  (expand-file-name
   (concat (file-name-as-directory
	    (file-name-directory (symbol-file #'ermine-python-path)))
	   "../lib")))

(defun ermine-get-connect-code (mel)
  (concat (format "import sys; sys.path.insert(0, '%s'); " (ermine-python-path))
	  "from ermine.maya_client import MayaScriptClient; "
	  (format "MayaScriptClient(mel=%s).run(); " (if mel "True" "False"))
	  "sys.exit(0)\n"))

(defun ermine-python-connect ()
  "Connect to a running maya process, and show an interactive
prompt in another buffer"
  (interactive)
  (if (python-shell-get-process)
      (switch-to-buffer-other-window (python-shell-get-buffer))

    (let ((python-shell-interpreter-args
	   (if (string= python-shell-interpreter "python3")
	       (format "%s %s" python-shell-interpreter-args "-q")
	     python-shell-interpreter-args)))

      (run-python)
      (python-shell-completion-native-turn-off)
      (python-shell-send-string (ermine-get-connect-code nil))

      (if (version< emacs-version "27.1")
	  (switch-to-buffer-other-window (python-shell-get-buffer))))))

(defun ermine-mel-is-comint-live ()
  (and ermine-mel-comint-buffer
       (process-live-p (get-buffer-process ermine-mel-comint-buffer))))

(defun ermine-mel-connect ()
  "Connect to a running maya process, and show an interactive
prompt in another buffer"
  (interactive)
  (if (ermine-mel-is-comint-live)
      (switch-to-buffer-other-window ermine-mel-comint-buffer)

    (let ((buf (apply 'make-comint
		      `("MEL" ,python-shell-interpreter nil "-i"
			,@(if (string= python-shell-interpreter "python3") (list "-q") nil)))))

      (with-current-buffer buf
	(local-set-key (kbd "C-c C-l") #'comint-clear-buffer)

	;; When the cursor is in the middle of the output, stop the
	;; return key from pasting the whole lot back and executing it
	(local-set-key (kbd (if (display-graphic-p) "<return>" "RET"))
		       (lambda ()
			 (interactive)
			 (if (comint-after-pmark-p)
			     (comint-send-input)
			   (message "Point is before process mark, NOT sending")))))

      (setq ermine-mel-comint-buffer buf)
      (comint-send-string (get-buffer-process buf) (ermine-get-connect-code t))
      (switch-to-buffer-other-window buf))))

(defun ermine-write-string-to-temp-file (string type)
  (let ((tmpfile (make-temp-file type nil (concat "." type))))
    (with-temp-file tmpfile
      (insert string))
    tmpfile))

(defun ermine-mel-send (begin end)
  (if (not (ermine-mel-is-comint-live))
      (message "Not connected to maya")

    (let* ((string (buffer-substring-no-properties begin end))
	   (tmpfile (ermine-write-string-to-temp-file string "mel"))
	   (code (format
		  (concat "print(\"\\n\"); "
			  "eval(\"source \\\"%s\\\"\"); "
			  "sysFile -del \"%s\"; ;\n")
		  tmpfile tmpfile))
	   (_ (string-match "\\`\n*\\(.*\\)" string)))

      (message "Sent: %s..." (match-string 1 string))
      (comint-send-string (get-buffer-process ermine-mel-comint-buffer) code))))

(defun ermine-mel-send-defun ()
  "Send the procedure/function the point is in to Maya"
  (interactive)
  (let ((begin (save-excursion
		 (c-beginning-of-defun)
		 (point)))
	(end (save-excursion
	       (c-beginning-of-defun)
	       (c-end-of-defun)
	       (point))))
    (ermine-mel-send begin end)))

(defun ermine-mel-send-statement ()
  "Send the statement before the point to maya"
  (interactive)
  (let ((begin (save-excursion
		 (c-beginning-of-statement-1)
		 (point)))
	(end (save-excursion
	       (c-beginning-of-statement-1)
	       (c-end-of-statement)
	       (point))))
    (ermine-mel-send begin end)))

(defun ermine-mel-send-region ()
  (interactive)
  (if (not (region-active-p))
      (message "No region active, can't send")
    (ermine-mel-send (region-beginning) (region-end))
    (message "Sent region")))

(defun ermine-mel-send-buffer ()
  (interactive)
  (save-restriction
    (widen)
    (ermine-mel-send (point-min) (point-max))) )


(defun ermine-mel-configure-buffer ()
  "Configure current buffer for MEL"
  (interactive)
  (c-mode)
  (local-set-key (kbd "C-c C-c") #'ermine-mel-send-buffer)
  (local-set-key (kbd "C-c C-r") #'ermine-mel-send-region)
  (local-set-key (kbd "C-c C-e") #'ermine-mel-send-statement)
  (local-set-key (kbd "C-M-x") #'ermine-mel-send-defun))

(add-to-list 'auto-mode-alist '("\\.mel\\'" . ermine-mel-configure-buffer))


(provide 'ermine)
