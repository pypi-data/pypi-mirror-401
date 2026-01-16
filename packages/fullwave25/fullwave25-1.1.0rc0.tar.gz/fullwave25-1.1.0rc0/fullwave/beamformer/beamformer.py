import numpy as np

# hilbert transform
from scipy.signal import hilbert

# function [dd] = focusProfile (fcen,coords,cfl)
# dd=zeros(size(coords,1),1);
# for i=1:length(fcen)
#   dd = dd + (coords(:,i)-fcen(i)).^2;
# end
# dd=sqrt(dd);
# %  dd = sqrt((coords(:,1)-fcen(1)).^2+(coords(:,2)-fcen(2)).^2+(coords(:,3)-fcen(3)).^2);
# dd = round(dd/cfl);
# dd = dd-min(dd);


class Beamformer:
    # https://github.com/gfpinton/fullwave_bmme890/blob/master/fullwave2_launcher_imaging_planewave.m
    def __init__(
        self,
        c0: float,
        dx: float,
        dt: float,
        lateral_position_m: np.ndarray,
        axial_position_m: np.ndarray,
        num_elements: int,
        transducer_coordinates: np.ndarray,
        f_number: float = 1.0,
    ):
        self.c0 = c0
        self.dx = dx
        self.dt = dt
        self.lateral_position_m = lateral_position_m
        self.axial_position_m = axial_position_m
        self.num_elements = num_elements
        self.transducer_coordinates = transducer_coordinates
        self.f_number = f_number

    def delay_and_sum(self, signals: np.ndarray) -> np.ndarray:
        # signals: [n_elements, n_time]
        n_time = signals.shape[1]
        hilbert_signals = hilbert(signals, axis=1)

        # [val idt0] = max(abs(hilbert(px)))
        # idps = cell(length(lats), length(deps));
        # for ii = 1:length(lats)
        #     lat = lats(ii);
        #     for jj = 1:length(deps)
        #         dep = deps(jj);
        #         fcen = round([lat / dY + mean(xducercoords(:, 1)) dep / dY]);
        #         idx = find(abs(xducercoords(:, 1) - fcen(1)) <= fcen(2) / fnumber);
        #         dd = focusProfile(fcen, xducercoords(idx, :), dT / dY * c0);
        #         idt = idt0 + round(2 * dep / double(c0) / (dT));
        #         %idt=idt0+round(dep/double(c0)/(dT)+(dep*cos(theta)+lat*sin(theta))/double(c0)/dT);
        #         idp = double((size(pxducer, 1) * (idx - 1)) + double(idt) + dd);
        #         idp = idp(find(idp > 0 & idp <= size(pxducer, 1) * size(pxducer, 2)));
        #         idps{ii, jj} = idp;
        #     end
        # end

        # for ii = 1:length(lats)
        #     for jj = 1:length(deps)
        #         bm(ii, jj, n) = sum(pxducer(idps{ii, jj}));
        #     end
        # end

        # test = np.max(np.abs(hilbert_signals))
        idt_0 = np.argmax(np.abs(hilbert_signals))
        idps = np.empty((len(self.lateral_position_m), len(self.axial_position_m)), dtype=object)
        for i_lat, lat in enumerate(self.lateral_position_m):
            for i_axial, axial in enumerate(self.axial_position_m):
                fcen = np.array(
                    [
                        int(axial / self.dx),
                        int(lat / self.dx + np.mean(self.transducer_coordinates[:, 1]) / self.dx),
                    ],
                )
                idx = np.where(
                    np.abs(self.transducer_coordinates[:, 0] / self.dx - fcen[0])
                    <= fcen[1] / self.f_number,
                )[0]

                dd = np.zeros(len(idx), dtype=int)

                for i in range(len(fcen)):
                    dd += np.round(
                        (self.transducer_coordinates[idx, i] - fcen[i]) ** 2,
                    ).astype(int)
                dd = np.sqrt(dd)
                dd = np.round(dd / (self.dt / self.dx * self.c0)).astype(int)
                dd = dd - dd.min()

                idt = idt_0 + int(2 * axial / self.c0 / self.dt)
                idp = (signals.shape[0] * (idx)) + idt + dd
                idp = idp[(idp > 0) & (idp <= signals.shape[0] * signals.shape[1])]
                idps[i_lat, i_axial] = idp
        beamformed_image = np.zeros((len(self.lateral_position_m), len(self.axial_position_m)))
        for i_lat in range(len(self.lateral_position_m)):
            for i_axial in range(len(self.axial_position_m)):
                beamformed_image[i_lat, i_axial] = np.sum(
                    hilbert_signals.flatten()[idps[i_lat, i_axial]],
                )
        return beamformed_image
