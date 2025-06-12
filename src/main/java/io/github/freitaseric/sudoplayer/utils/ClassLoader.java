package io.github.freitaseric.sudoplayer.utils;

import io.github.classgraph.ClassGraph;
import io.github.classgraph.ClassInfo;
import io.github.classgraph.ClassInfoList;
import io.github.classgraph.ScanResult;
import io.github.freitaseric.sudoplayer.internal.exceptions.LoaderException;

import java.util.HashMap;

public class ClassLoader {
    @SuppressWarnings("unchecked")
    public static <K, V> HashMap<K, V> loadClasses(final String packageName, String getKeyMethodName, final Class<?> clazz) throws LoaderException {
        HashMap<K, V> map = new HashMap<>();

        try (ScanResult scanResult = new ClassGraph().enableAllInfo().acceptPackages(packageName).scan()) {
            ClassInfoList classes = scanResult.getClassesImplementing(clazz);

            for (ClassInfo classInfo : classes) {
                try {
                    V instance = (V) classInfo.loadClass().getDeclaredConstructor().newInstance();

                    map.put((K) instance.getClass().getMethod(getKeyMethodName).invoke(instance), instance);
                } catch (Exception e) {
                    throw new LoaderException("Could not load instance of class " + clazz.getSimpleName() + " from " + packageName, e);
                }
            }
        } catch (Exception e) {
            throw new LoaderException("Could not load class " + clazz.getSimpleName() + " from " + packageName, e);
        }

        return map;
    }
}
