(setq t1 '(and (or A B (not C)) (or (not A) D) (or (not B))))
(setq t2 '(and (or (not p) q) (or (not q) r) (or (not r)) (or p)))

(defun unique (in &optional out)
  (cond 
    ((null in) out)
    ((member (car in) out :test #'equal) (unique (cdr in) out))
    (t (unique (cdr in) (cons (car in) out)))))

(defun resolve-atom-body (a b-hd b-tl)
  (cond 
    ((null b-hd) b-tl)
    ((equal a (car b-hd)) (resolve-atom-body a (cdr b-hd) b-tl))
    (t (resolve-atom-body a (cdr b-hd) (cons (car b-hd) b-tl)))))

(defun resolve-atom (a b)
  (let ((match-a (if (listp a) (cadr a) (list 'not a))))
    (resolve-atom-body match-a b '())))

(defun set-equal (s1 s2)
  (and (not (set-difference s1 s2))
       (not (set-difference s2 s1))))

(defun resolve (a b &optional result)
  (cond
    ((null a) (unique (append b result)))
    ((null b) (unique (append a result)))
    (t (let ((new-b (resolve-atom (car a) b)))
         (if (set-equal new-b b)
             (resolve (cdr a) b (cons (car a) result))
             (resolve (cdr a) new-b result))))))

(defun do-resolves (a bs)
  (if (null bs) 
      nil
      (let ((r (resolve a (car bs)))
            (not-r (union a (car bs) :test #'equal)))
        (if (> (length not-r) (length r)) ; resolution
            (cons r (do-resolves a (cdr bs)))
            (do-resolves a (cdr bs))))))

(defun refute-body (given orig-given generated)
  (cond
    ((and (null (cdr given)) (subsetp generated orig-given :test #'equal)) nil)
    ((null (cdr given))
      (let ((t1 (union generated orig-given :test #'equal))) 
        (refute-body t1 t1 '())))
    (t 
      (let ((rs (do-resolves (car given) (cdr given))))
        (if (and (not (null rs)) (some #'null rs))
            (car given) ;; contradiction
            (refute-body (cdr given) 
                         orig-given 
                         (union rs generated :test #'equal)))))))

(defun strip-ands-and-ors (cnf)
  (mapcar #'cdr (cdr cnf)))

(defun refute (cnf)
  ;; strip off the initial and and all the ors.  they get in the way
  (let ((good-cnf (strip-ands-and-ors cnf)))
    (refute-body good-cnf good-cnf '())))

(defun resolution-refutation (cnf)
  (refute cnf))

