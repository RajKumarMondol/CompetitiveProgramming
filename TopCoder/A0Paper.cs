using System;

namespace TopCoder
{
    public class A0Paper
    {
        public string canBuild(int[] input)
        {
            for (int index = input.Length - 1; index > 0; index--)
            {
                input[index - 1] += input[index] / 2;
            }
            if (input[0] > 0)
                return "Possible";
            return "Impossible";
        }
    }
}
