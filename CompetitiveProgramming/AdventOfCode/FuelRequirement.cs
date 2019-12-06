using System;

namespace CompetitiveProgramming.AdventOfCode
{
    public class FuelRequirement
    {
        public long calculateFuelForMass(int[] moduleMasses)
        {
            long totalFuelRequirement = 0;
            foreach (int moduleMass in moduleMasses)
            {
                totalFuelRequirement += getFuelRequirement(moduleMass);
            }
            return totalFuelRequirement;
        }

        private int getFuelRequirement(int moduleMass)
        {
            return (moduleMass / 3 - 2);
        }
    }
}