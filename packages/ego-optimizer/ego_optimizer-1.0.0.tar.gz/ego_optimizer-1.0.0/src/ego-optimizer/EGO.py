import numpy as np

class EGO:
    """
    Entropy-Guided Optimization (EGO).
    
    Mechanism:
    Uses Population Entropy to adaptively control the Mutation Factor (F)
    and Crossover Rate (CR). 
    - High Entropy -> High F/CR (Exploration)
    - Low Entropy  -> Low F/CR (Exploitation)
    """
    def __init__(self, func, dim, pop_size=50, max_iter=1500, lb=-100, ub=100,
                 seed=None, **kwargs):
        self.func = func
        self.dim = dim
        self.pop_size = pop_size
        self.max_iter = max_iter
        self.lb = np.array([lb] * dim)
        self.ub = np.array([ub] * dim)
        self.rng = np.random.default_rng(seed)

        # Initialize Population
        self.X = self.rng.uniform(self.lb, self.ub, size=(self.pop_size, self.dim))
        self.Y = np.array([self.func(x) for x in self.X])

        # Track Best
        self.best_idx = np.argmin(self.Y)
        self.best_x = self.X[self.best_idx].copy()
        self.best_y = self.Y[self.best_idx]
        self.history = [self.best_y]

    def _calculate_entropy(self):
        """Calculates normalized Shannon entropy (0.0 to 1.0)."""
        # Linear Ranking
        worst_y = np.max(self.Y)
        scores = worst_y - self.Y 
        
        total_score = np.sum(scores)
        if total_score == 0:
            return 0.0 # Zero diversity
            
        probs = scores / total_score
        probs = np.clip(probs, 1e-15, 1.0) # Clip for log safety
        
        entropy = -np.sum(probs * np.log(probs))
        max_entropy = np.log(self.pop_size)
        
        return entropy / max_entropy if max_entropy > 0 else 0

    def optimize(self):
        for t in range(self.max_iter):
            # --- 1. Calculate Entropy State ---
            w = self._calculate_entropy()
            
            # --- 2. Adaptive Parameters (The Secret Sauce) ---
            # If High Entropy (Explore): F->0.9, CR->0.9
            # If Low Entropy (Converge): F->0.1, CR->0.1
            # We keep a base of 0.1 so it never freezes completely.
            current_F = 0.1 + (0.8 * w)
            current_CR = 0.1 + (0.8 * w)
            
            # --- 3. Mutation (DE/rand/1) ---
            # We use the Adaptive F here
            idxs = self.rng.integers(0, self.pop_size, size=(self.pop_size, 3))
            a = self.X[idxs[:, 0]]
            b = self.X[idxs[:, 1]]
            c = self.X[idxs[:, 2]]
            
            V_mutant = a + current_F * (b - c)
            
            # --- 4. Crossover ---
            # We use the Adaptive CR here
            cross_mask = self.rng.random(size=(self.pop_size, self.dim)) < current_CR
            U = np.where(cross_mask, V_mutant, self.X)
            
            # --- 5. Bounds & Selection ---
            U = np.clip(U, self.lb, self.ub)
            Y_new = np.array([self.func(u) for u in U])
            
            # Greedy Selection
            improved_mask = Y_new < self.Y
            self.X[improved_mask] = U[improved_mask]
            self.Y[improved_mask] = Y_new[improved_mask]
            
            # Update Global Best
            current_min = np.min(self.Y)
            if current_min < self.best_y:
                self.best_y = current_min
                self.best_x = self.X[np.argmin(self.Y)].copy()
                
            self.history.append(self.best_y)
            
        return self.best_x, self.best_y, self.history

# Wrapper to keep your Test.py working
def entropy_guided_optimization(func, dim, pop_size=50, max_iter=1500, lb=-100, ub=100, 
                                F=None, mutation_rate=None, seed=None):
    # Note: F and mutation_rate are ignored here because they are Adaptive now.
    optimizer = EGO(func, dim, pop_size, max_iter, lb, ub, seed=seed)
    return optimizer.optimize()