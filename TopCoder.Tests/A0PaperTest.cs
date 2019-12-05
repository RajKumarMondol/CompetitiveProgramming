using System;
using Xunit;

namespace TopCoder.Tests
{
    public class A0PaperTest
    {
        [Theory]
        //TopCoder Test Data
        [InlineData(new int[] { 0, 3 }, "Possible")]
        [InlineData(new int[] { 0, 1, 2 }, "Possible")]
        [InlineData(new int[] { 0, 0, 0, 0, 15 }, "Impossible")]
        [InlineData(new int[] { 2, 0, 0, 0, 0, 0, 0, 3, 2, 0, 0, 5, 0, 3, 0, 0, 1, 0, 0, 0, 5 }, "Possible")]
        //Personal Test Data
        [InlineData(new int[] { 0, 1, 0, 4 }, "Possible")]
        public void Test(int[] input, string expectedOutput)
        {
            var a0Paper = new A0Paper();
            string output = a0Paper.canBuild(input);
            Assert.Equal(expectedOutput, output);
        }
    }
}
