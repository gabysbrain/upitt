
;;; variables are atoms that start with ?
(defun var? (x) (and (atom x) (equal (subseq (string x) 0 1) "?")))

(defun cnf-unique (exp)
  (cond
    ((null exp) '())
    ((member (car exp) (cdr exp) :test #'equal) (cnf-unique (cdr exp)))
    ((atom (car exp)) (cons (car exp) (cnf-unique (cdr exp))))
    (t (cons (cnf-unique (car exp)) (cnf-unique (cdr exp))))))

(defun match (pattern expression)
  (match-body pattern expression '((match . t))))

(defun match-body (pat exp bdgs)
  (cond 
    ((eql pat exp) bdgs) ;; atomic matching
    ((var? pat) (bind-var pat exp bdgs)) ;; down to single variable
    ((or (atom pat) (atom exp)) nil) ;; unmatched atoms
    (t (let ((new-bdgs (match-body (car pat) (car exp) bdgs)))
         (when new-bdgs (match-body (cdr pat) (cdr exp) new-bdgs))))))

(defun bind-var (var exp bdgs)
  (let ((tmpval (assoc var bdgs))) ;; see if var is already defined
    (cond 
      ((null tmpval) (acons var exp bdgs)) ;; unbound var
      ((equal exp (cdr tmpval)) bdgs) ;; current binding is equal
      (t nil))))

;;; given a list of bindings and a pattern, replace the variables 
;;; in the pattern with the bindings from bindings
(defun rewrite (pattern bindings)
  (cond
    ((var? pattern) (cdr (assoc pattern bindings))) ;; replace var with binding
    ((atom pattern) pattern) ;; keep atoms
    (t (cons (rewrite (car pattern) bindings) 
             (rewrite (cdr pattern) bindings)))))

;;; Given a pattern, replacement and expression, recursively go through
;;; the expression until something matches.  If so, replace it.
(defun rec-convert (pat repl exp)
  (let ((bdgs (match pat exp)))
    (cond
      ((null exp) '())
      (bdgs (rewrite repl bdgs))
      ((atom exp) exp)
      (t (cons (rec-convert pat repl (car exp)) 
               (rec-convert pat repl (cdr exp)))))))

;;; Tries to convert an expression with every pattern
(defun convert-patterns (pats exp)
  (if (null pats)
      exp
      (let ((pat (car (car pats)))
            (repl (cadr (car pats))))
        (convert-patterns (cdr pats) (rec-convert pat repl exp)))))

(defun collapse-lev-1 (sym exp)
  ;(print sym)
  ;(print exp)
  ;(print "collapse") (print exp)
  (cond
    ((null exp) '())
    ((or (atom exp) (atom (car exp))) exp)
    ((eq sym (caar exp)) (append (cdar exp) (collapse-lev-1 sym (cdr exp))))
    (t (append (list (car exp)) (collapse-lev-1 sym (cdr exp))))))

;; collapse nested lists starting with sym into one list
(defun collapse-sym (exp)
  (print exp)
  (if (or (null exp) (atom exp)) 
      exp
      (let ((fix-rest (mapcar #'collapse-sym (cdr exp))))
        (print "rest")
        (print fix-rest)
        (print (collapse-lev-1 (car exp) fix-rest))
        (cons (car exp) (collapse-lev-1 (car exp) fix-rest)))))

;;; All the patterns we want to replace
(setf *cnf-patterns*
  '(((not (not ?x))      ?x) ;; double negation
    ((bic ?x ?y)         (and (cond ?x ?y) (cond ?y ?x))) ;; biconditional
    ((impl ?x ?y)        (or (not ?x) ?y)) ;; implication
    ((not (or ?x ?y))    (and (not ?x) (not ?y))) ;; demorgan's #1
    ((not (and ?x ?y))   (or (not ?x) (not ?y))) ;; demorgan's #2
    ((or ?x (and ?y ?z)) (and (or ?y ?x) (or ?z ?x))) ;; distribution #1
    ((or (and ?y ?z) ?x) (and (or ?y ?x) (or ?z ?x))))) ;; distribution #2

;;; Converts an expression to cnf.  Keeps calling itself until the
;;; expression is completely converted
(defun convert2cnf (exp)
  (let ((new-exp (convert-patterns *cnf-patterns* exp)))
    (if (equal exp new-exp) 
        (cnf-unique (collapse-sym (cons 'and exp)))
        (convert2cnf new-exp))))

