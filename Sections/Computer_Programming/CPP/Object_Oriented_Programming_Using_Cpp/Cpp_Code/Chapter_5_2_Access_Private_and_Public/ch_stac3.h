struct ch_stack {
    public:
        void reset ()       { top = EMPTY; }
        void push (char c)  { top++; s[top] = c; }
        char pop ()         { return s[top--]; }
        char top_of ()      { return s[top]; }
        bool empty ()      { return ( top == EMPTY ); }
        bool full ()        { return ( top == FULL  ); }

    private:
        enum 
        {  
            max_len = 100,
            EMPTY = -1,
            FULL = max_len-1
                
        };

        char s[max_len];
        int top;
};