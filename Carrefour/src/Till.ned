package carrefour;

//Till is the module representing a till of the supermarket.
//Its behavior and structure do not depend on the policy used.
simple Till
{
    parameters:
    	//position represents the position of the till in the row of tills
        int position;
        @signal[numCustomersQueue] (type=long);
        @statistic[stats_numCustomersQueue] (source="numCustomersQueue"; record=timeavg;);
        
    gates:
    	//customers come in the till through this gate after being sorted by Decider module
        input in;
}









